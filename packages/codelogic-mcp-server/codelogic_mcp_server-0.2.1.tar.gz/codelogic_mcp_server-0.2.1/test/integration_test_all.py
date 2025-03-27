import os
import sys
import unittest
import asyncio
import mcp.types as types

# Add the parent directory to Python path to make the absolute import work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use absolute import instead of relative import
from test.test_fixtures import setup_test_environment
from codelogic_mcp_server.utils import get_method_nodes, get_impact
from codelogic_mcp_server.utils import get_method_nodes

class TestHandleCallToolIntegration(unittest.TestCase):

    def test_handle_call_tool_get_impact_multi_app_java(self):
        # Setup environment before importing modules that use it
        env_vars = {
            'CODELOGIC_MV_NAME': 'SalaryApp',
            'CODELOGIC_SERVER_HOST': 'https://demo.panopticops.net',
            'CODELOGIC_USERNAME': 'ai@codelogic.com',
            'CODELOGIC_PASSWORD': '1AIAIAIai'
        }
        handle_call_tool, *_ = setup_test_environment(env_vars)
        
        async def run_test():
            result = await handle_call_tool('get-impact', {'method': 'addPrefix', 'class': 'CompanyInfo'})

            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            self.assertIsInstance(result[0], types.TextContent)
            with open('impact_analysis_result_multi_app_java.md', 'w', encoding='utf-8') as file:
                file.write(result[0].text)
            self.assertIn("# Impact Analysis for Method: `addPrefix`", result[0].text)

        asyncio.run(run_test())

    def test_handle_call_tool_get_impact_dotnet(self):
        # Setup environment before importing modules that use it
        env_vars = {
            'CODELOGIC_MV_NAME': 'IDE Integration Workspace',
            'CODELOGIC_SERVER_HOST': 'https://dogfood.app.codelogic.com',
            'CODELOGIC_USERNAME': 'temporaryadmin@codelogic.com',
            'CODELOGIC_PASSWORD': 'hae5kjf8vwz-RKX8yzt'
        }
        handle_call_tool, *_ = setup_test_environment(env_vars)
        
        async def run_test():
            result = await handle_call_tool('get-impact', {'method': 'IsValid', 'class': 'AnalysisOptionsValidator'})

            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            self.assertIsInstance(result[0], types.TextContent)
            with open('impact_analysis_result_dotnet.md', 'w', encoding='utf-8') as file:
                file.write(result[0].text)
            self.assertIn("# Impact Analysis for Method: `IsValid`", result[0].text)

        asyncio.run(run_test())

class TestUtils(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Setup environment variables and get the utility functions
        env_vars = {
            'CODELOGIC_MV_NAME': 'IDE Integration Workspace',
            'CODELOGIC_SERVER_HOST': 'https://dogfood.app.codelogic.com',
            'CODELOGIC_USERNAME': 'temporaryadmin@codelogic.com',
            'CODELOGIC_PASSWORD': 'hae5kjf8vwz-RKX8yzt'
        }
        
        # Import and initialize all required functions
        _, get_mv_definition_id, get_mv_id_from_def, get_method_nodes, get_impact, authenticate = setup_test_environment(env_vars)
        
        cls.token = authenticate()
        cls.mv_name = os.getenv('CODELOGIC_MV_NAME', 'Default')
        cls.mv_def_id = get_mv_definition_id(cls.mv_name, cls.token)
        cls.mv_id = get_mv_id_from_def(cls.mv_def_id, cls.token)
        cls.nodes = get_method_nodes(cls.mv_id, 'IsValid')

    def test_authenticate(self):
        self.assertIsNotNone(self.token)

    def test_get_mv_definition_id(self):
        self.assertRegex(self.mv_def_id, r'^[0-9a-fA-F-]{36}$')

    def test_get_mv_id_from_def(self):
        self.assertRegex(self.mv_id, r'^[0-9a-fA-F-]{36}$')

    def test_get_method_nodes(self):
        self.assertIsInstance(self.nodes, list)

    def test_get_impact(self):
        node_id = self.nodes[0]['id'] if self.nodes else None
        self.assertIsNotNone(node_id, "Node ID should not be None")
        impact = get_impact(node_id)
        self.assertIsInstance(impact, str)

if __name__ == '__main__':
    unittest.main()

