from flask import Flask, request, jsonify
import os
import json
import requests
from openai import OpenAI
from typing import Dict, Any, Callable, Optional

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ToolRegistry:
    """Manages the available tools/functions that can be called by the MCP server."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
    
    def register(self, name: str, handler: Callable) -> None:
        """Register a new tool with the registry."""
        self.tools[name] = handler
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        """List all available tools."""
        return list(self.tools.keys())


class ContextManager:
    """Manages conversation context for different sessions."""
    
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}
    
    def get_context(self, session_id: str) -> Dict[str, Any]:
        """Get or create context for a session."""
        if not session_id:
            return {}
        
        if session_id not in self.contexts:
            self.contexts[session_id] = {}
        
        return self.contexts[session_id]
    
    def update_context(self, session_id: str, context_update: Dict[str, Any]) -> None:
        """Update the context for a session."""
        current_context = self.get_context(session_id)
        current_context.update(context_update)
        self.contexts[session_id] = current_context


class MCPServer:
    """Model Context Protocol server implementation."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.context_manager = ContextManager()
        self.tool_registry = ToolRegistry()
        
        # Register tools
        self.register_tools()
        
        # Setup routes
        self.setup_routes()
    
    def register_tools(self):
        """Register available tools with the tool registry."""
        
        def execute_api_call(json_data: Dict[str, Any]) -> Dict[str, Any]:
            """Execute a call to the external API endpoint."""
            try:
                response = requests.post(
                    "https://your-api-endpoint.com/action",
                    json=json_data,
                    headers={"Content-Type": "application/json"}
                )
                return response.json()
            except Exception as e:
                return {"error": str(e)}
        
        # Register the external API endpoint as a tool
        self.tool_registry.register("execute_api_call", execute_api_call)
    
    def setup_routes(self):
        """Setup the Flask routes."""
        
        @self.app.route("/api/process", methods=["POST"])
        def process():
            try:
                data = request.json
                text = data.get("text")
                session_id = data.get("session_id", "default")
                
                if not text:
                    return jsonify({"error": "Text input is required"}), 400
                
                # Get or create context for this session
                context = self.context_manager.get_context(session_id)
                
                # Process the request using MCP pattern
                result = self.process_with_mcp(text, context)
                
                # Update context with this interaction
                self.context_manager.update_context(
                    session_id,
                    {
                        "last_input": text,
                        "last_output": result,
                        "timestamp": {"$date": datetime.datetime.now().isoformat()}
                    }
                )
                
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
    def process_with_mcp(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process text input using the MCP pattern."""
        # 1. Generate structured JSON from natural language using OpenAI
        structured_data = self.generate_structured_json(text, context)
        
        # 2. Validate the generated JSON
        validated_data = self.validate_json(structured_data)
        
        # 3. Determine which tool to use
        tool_name = self.determine_tool_from_json(validated_data)
        tool = self.tool_registry.get_tool(tool_name)
        
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        # 4. Execute the tool with the structured data
        return tool(validated_data)
    
    def generate_structured_json(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON from natural language using OpenAI."""
        response = openai_client.chat.completions.create(
            model="gpt-4",  # or your preferred model
            messages=[
                {
                    "role": "system",
                    "content": f"""You translate user text into structured JSON for API calls. 
                        Format the JSON according to these specifications: 
                        [Include your API's JSON schema here]
                        
                        Context from previous interactions:
                        {json.dumps(context)}"""
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        json_string = response.choices[0].message.content
        return json.loads(json_string)
    
    def validate_json(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated JSON."""
        # Implement validation logic here
        # You could use a library like pydantic or jsonschema for validation
        return json_data
    
    def determine_tool_from_json(self, json_data: Dict[str, Any]) -> str:
        """Determine which tool to use based on the JSON content."""
        # Logic to determine which tool to use
        # For now, we'll always use the execute_api_call tool
        return "execute_api_call"
    
    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the MCP server."""
        self.app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    import datetime
    
    # Create and start the server
    mcp_server = MCPServer()
    mcp_server.run(port=5000, debug=True)
