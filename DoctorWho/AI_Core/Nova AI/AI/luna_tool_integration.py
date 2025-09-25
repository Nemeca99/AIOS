"""
Luna Tool Integration System
Integrates tool calling capabilities with Luna's response generation
"""

import json
import logging
from typing import Dict, List, Any, Optional
from app.tools.luna_tools import LunaTools

logger = logging.getLogger(__name__)

class LunaToolIntegration:
    """Integrates tool calling with Luna's AI responses"""
    
    def __init__(self):
        self.tools = LunaTools()
        self.tool_schemas = self.tools.get_tool_schema()
    
    def get_tool_schemas(self) -> List[Dict]:
        """Get tool schemas for function calling"""
        return self.tool_schemas
    
    def parse_tool_calls(self, response_text: str) -> List[Dict]:
        """Parse tool calls from Luna's response"""
        tool_calls = []
        
        # Look for tool call patterns in the response
        # Pattern: <tool_call name="tool_name" params='{"param": "value"}'></tool_call>
        import re
        
        tool_pattern = r'<tool_call\s+name="([^"]+)"\s+params=\'([^\']+)\'><\/tool_call>'
        matches = re.findall(tool_pattern, response_text)
        
        for tool_name, params_json in matches:
            try:
                params = json.loads(params_json)
                tool_calls.append({
                    "name": tool_name,
                    "parameters": params
                })
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool call parameters: {params_json}")
                continue
        
        return tool_calls
    
    def execute_tool_calls(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute tool calls and return results"""
        results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            parameters = tool_call["parameters"]
            
            logger.info(f"Executing tool: {tool_name} with params: {parameters}")
            
            try:
                result = self.tools.execute_tool(tool_name, **parameters)
                results.append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": result,
                    "success": "error" not in result
                })
            except Exception as e:
                results.append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": {"error": f"Tool execution failed: {str(e)}"},
                    "success": False
                })
        
        return results
    
    def format_tool_results(self, tool_results: List[Dict]) -> str:
        """Format tool results for display"""
        if not tool_results:
            return ""
        
        formatted_results = "\n\n**Tool Results:**\n"
        
        for i, result in enumerate(tool_results, 1):
            tool_name = result["tool_name"]
            success = result["success"]
            tool_result = result["result"]
            
            status = "✅" if success else "❌"
            formatted_results += f"\n{i}. {status} **{tool_name}**\n"
            
            if success:
                if isinstance(tool_result, dict):
                    if "success" in tool_result and tool_result["success"]:
                        # Format successful results
                        for key, value in tool_result.items():
                            if key != "success":
                                formatted_results += f"   - {key}: {value}\n"
                    else:
                        formatted_results += f"   - Result: {tool_result}\n"
                else:
                    formatted_results += f"   - Result: {tool_result}\n"
            else:
                formatted_results += f"   - Error: {tool_result.get('error', 'Unknown error')}\n"
        
        return formatted_results
    
    def process_response_with_tools(self, response_text: str) -> str:
        """Process Luna's response and execute any tool calls"""
        # Parse tool calls from the response
        tool_calls = self.parse_tool_calls(response_text)
        
        if not tool_calls:
            return response_text
        
        # Execute tool calls
        tool_results = self.execute_tool_calls(tool_calls)
        
        # Format and append results
        formatted_results = self.format_tool_results(tool_results)
        
        # Remove tool call markers from the original response
        import re
        clean_response = re.sub(r'<tool_call[^>]*><\/tool_call>', '', response_text)
        
        return clean_response + formatted_results
    
    def get_available_tools_info(self) -> str:
        """Get information about available tools"""
        info = "**Available Tools:**\n\n"
        
        for schema in self.tool_schemas:
            function = schema["function"]
            name = function["name"]
            description = function["description"]
            
            info += f"**{name}**: {description}\n"
            
            if "parameters" in function and "properties" in function["parameters"]:
                properties = function["parameters"]["properties"]
                if properties:
                    info += "  Parameters:\n"
                    for param_name, param_info in properties.items():
                        param_desc = param_info.get("description", "")
                        param_type = param_info.get("type", "")
                        required = param_name in function["parameters"].get("required", [])
                        req_text = " (required)" if required else " (optional)"
                        info += f"    - {param_name} ({param_type}): {param_desc}{req_text}\n"
            
            info += "\n"
        
        return info
    
    def create_tool_usage_examples(self) -> str:
        """Create examples of how to use tools"""
        examples = "**Tool Usage Examples:**\n\n"
        
        examples += "1. **File Operations:**\n"
        examples += "   - Read a file: <tool_call name=\"file_read\" params='{\"file_path\": \"example.txt\"}'></tool_call>\n"
        examples += "   - Write a file: <tool_call name=\"file_write\" params='{\"file_path\": \"output.txt\", \"content\": \"Hello World\"}'></tool_call>\n"
        examples += "   - List directory: <tool_call name=\"file_list\" params='{\"directory_path\": \".\"}'></tool_call>\n\n"
        
        examples += "2. **Web Search:**\n"
        examples += "   - Search web: <tool_call name=\"web_search\" params='{\"query\": \"Python programming\", \"num_results\": 5}'></tool_call>\n\n"
        
        examples += "3. **Calculations:**\n"
        examples += "   - Calculate: <tool_call name=\"calculate\" params='{\"expression\": \"2 + 2 * 3\"}'></tool_call>\n\n"
        
        examples += "4. **System Info:**\n"
        examples += "   - Get system info: <tool_call name=\"system_info\" params='{\"info_type\": \"memory\"}'></tool_call>\n\n"
        
        examples += "5. **Code Execution:**\n"
        examples += "   - Run Python code: <tool_call name=\"code_execution\" params='{\"code\": \"print(Hello World)\"}'></tool_call>\n\n"
        
        return examples
