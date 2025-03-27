import os
import importlib

# Base test environment setup
os.environ['CODELOGIC_TEST_MODE'] = 'true'

def setup_test_environment(env_vars):
    """Set environment variables and reload affected modules"""
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    # Import and reload modules that may have cached environment variables
    if any(k in env_vars for k in ['CODELOGIC_SERVER_HOST', 'CODELOGIC_USERNAME', 'CODELOGIC_PASSWORD', 'CODELOGIC_MV_NAME']):
        import codelogic_mcp_server.utils
        importlib.reload(codelogic_mcp_server.utils)
    
    # Only import handlers after environment is properly configured
    import codelogic_mcp_server.handlers
    importlib.reload(codelogic_mcp_server.handlers)
    
    # Return the imported modules for convenience
    from codelogic_mcp_server.handlers import handle_call_tool
    from codelogic_mcp_server.utils import (
        get_mv_definition_id, 
        get_mv_id_from_def,
        get_method_nodes,
        get_impact,
        authenticate
    )
    
    return handle_call_tool, get_mv_definition_id, get_mv_id_from_def, get_method_nodes, get_impact, authenticate
