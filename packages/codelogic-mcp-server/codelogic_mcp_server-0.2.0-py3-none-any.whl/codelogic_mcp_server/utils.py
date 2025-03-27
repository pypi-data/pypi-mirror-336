import os
import sys
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from neo4j import GraphDatabase

# Cache TTL settings from environment variables (in seconds)
TOKEN_CACHE_TTL = int(os.getenv('CODELOGIC_TOKEN_CACHE_TTL', '3600'))  # Default 1 hour
METHOD_CACHE_TTL = int(os.getenv('CODELOGIC_METHOD_CACHE_TTL', '300'))  # Default 5 minutes
IMPACT_CACHE_TTL = int(os.getenv('CODELOGIC_IMPACT_CACHE_TTL', '300'))  # Default 5 minutes

# Timeout settings from environment variables (in seconds)
REQUEST_TIMEOUT = float(os.getenv('CODELOGIC_REQUEST_TIMEOUT', '120.0'))
CONNECT_TIMEOUT = float(os.getenv('CODELOGIC_CONNECT_TIMEOUT', '30.0'))

# Cache storage
_cached_token = None
_token_expiry = None
_method_nodes_cache: Dict[str, tuple[List[Any], datetime]] = {}
_impact_cache: Dict[str, tuple[str, datetime]] = {}

# Configure HTTP client with improved settings
_client = httpx.Client(
    timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=CONNECT_TIMEOUT),
    limits=httpx.Limits(max_keepalive_connections=20, max_connections=30),
    transport=httpx.HTTPTransport(retries=3)
)

def find_node_by_id(nodes, id):
    for node in nodes:
        if node['id'] == id:
            return node
    return None

def get_mv_id(mv_name):
    token = authenticate()
    mv_def_id = get_mv_definition_id(mv_name, token)
    return get_mv_id_from_def(mv_def_id, token)

def get_mv_definition_id(mv_name, token):
    url = f"{os.getenv('CODELOGIC_SERVER_HOST')}/codelogic/server/materialized-view-definition/name?name={mv_name}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = _client.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']['id']

def get_mv_id_from_def(mv_def_id, token):
    url = f"{os.getenv('CODELOGIC_SERVER_HOST')}/codelogic/server/materialized-view/latest?definitionId={mv_def_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = _client.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']['id']

def get_method_nodes(materialized_view_id, short_name):
    cache_key = f"{materialized_view_id}:{short_name}"
    now = datetime.now()

    # Check cache
    if cache_key in _method_nodes_cache:
        nodes, expiry = _method_nodes_cache[cache_key]
        if now < expiry:
            sys.stderr.write(f"Method nodes cache hit for {short_name}\n")
            return nodes
        else:
            sys.stderr.write(f"Method nodes cache expired for {short_name}\n")

    try:
        token = authenticate()
        url = f"{os.getenv('CODELOGIC_SERVER_HOST')}/codelogic/server/ai-retrieval/search/shortname"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {token}"
        }
        params = {
            "materializedViewId": materialized_view_id,
            "shortname": short_name
        }
        
        sys.stderr.write(f"Requesting method nodes for {short_name} with timeout {REQUEST_TIMEOUT}s\n")
        response = _client.post(url, headers=headers, params=params, data={})
        response.raise_for_status()
        
        # Cache result
        nodes = response.json()['data']
        _method_nodes_cache[cache_key] = (nodes, now + timedelta(seconds=METHOD_CACHE_TTL))
        sys.stderr.write(f"Method nodes cached for {short_name} with TTL {METHOD_CACHE_TTL}s\n")
        return nodes
    except httpx.TimeoutException as e:
        sys.stderr.write(f"Timeout error fetching method nodes for {short_name}: {e}\n")
        # Return empty list instead of raising exception
        return []
    except httpx.HTTPStatusError as e:
        sys.stderr.write(f"HTTP error {e.response.status_code} fetching method nodes for {short_name}: {e}\n")
        # Return empty list instead of raising exception
        return []
    except Exception as e:
        sys.stderr.write(f"Error fetching method nodes: {e}\n")
        # Return empty list instead of raising exception
        return []

def extract_relationships(impact_data):
    relationships = []
    for rel in impact_data['data']['relationships']:
        start_node = find_node_by_id(impact_data['data']['nodes'], rel['startId'])
        end_node = find_node_by_id(impact_data['data']['nodes'], rel['endId'])
        if start_node and end_node:
            relationship = f"- {start_node['identity']} ({rel['type']}) -> {end_node['identity']}"
            relationships.append(relationship)
    return relationships

def get_impact(id):
    now = datetime.now()

    # Check cache
    if id in _impact_cache:
        impact, expiry = _impact_cache[id]
        if now < expiry:
            sys.stderr.write(f"Impact cache hit for {id}\n")
            return impact
        else:
            sys.stderr.write(f"Impact cache expired for {id}\n")

    token = authenticate()
    url = f"{os.getenv('CODELOGIC_SERVER_HOST')}/codelogic/server/dependency/impact/full/{id}/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = _client.get(url, headers=headers)
    response.raise_for_status()
    
    result = strip_unused_properties(response)
    
    # Cache result
    _impact_cache[id] = (result, now + timedelta(seconds=IMPACT_CACHE_TTL))
    sys.stderr.write(f"Impact cached for {id} with TTL {IMPACT_CACHE_TTL}s\n")
    return result

def strip_unused_properties(response):
    data = json.loads(response.text)
    
    # Strip out specific fields
    for node in data.get('data', {}).get('nodes', []):
        properties = node.get('properties', {})
        properties.pop('agentIds', None)
        properties.pop('sourceScanContextIds', None)
        properties.pop('isScanRoot', None)
        properties.pop('transitiveSourceNodeId', None)
        properties.pop('dataSourceId', None)
        properties.pop('scanContextId', None)
        properties.pop('id', None)
        properties.pop('shortName', None)
        properties.pop('materializedViewId', None)
        properties.pop('statistics.impactScore', None)
        properties.pop('codelogic.quality.impactScore', None)
        properties.pop('identity', None)
        properties.pop('name', None)
    
    return json.dumps(data)

def extract_nodes(impact_data):
    nodes = []
    for node in impact_data.get('data', {}).get('nodes', []):
        node_info = {
            'id': node.get('id'),
            'identity': node.get('identity'),
            'name': node.get('name'),
            'primaryLabel': node.get('primaryLabel'),
            'properties': node.get('properties', {})
        }
        nodes.append(node_info)
    return nodes

def authenticate():
    global _cached_token, _token_expiry
    now = datetime.now()
    
    # Return cached token if still valid
    if _cached_token is not None and _token_expiry is not None:
        if now < _token_expiry:
            sys.stderr.write("Using cached authentication token\n")
            return _cached_token
        else:
            sys.stderr.write("Authentication token expired\n")

    url = f"{os.getenv('CODELOGIC_SERVER_HOST')}/codelogic/server/authenticate"
    data = {
        "grant_type": "password",
        "username": os.getenv("CODELOGIC_USERNAME"),
        "password": os.getenv("CODELOGIC_PASSWORD")
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    try:
        response = _client.post(url, data=data, headers=headers)
        response.raise_for_status()
        _cached_token = response.json()['access_token']
        _token_expiry = now + timedelta(seconds=TOKEN_CACHE_TTL)
        sys.stderr.write(f"New authentication token cached with TTL {TOKEN_CACHE_TTL}s\n")
        return _cached_token
    except Exception as e:
        sys.stderr.write(f"Authentication error: {e}\n")
        raise
