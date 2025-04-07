import express from 'express';
import { OpenAI } from 'openai';
import { MCPServer, ContextManager, ToolRegistry } from './mcp';

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Create MCP Server
class ApplicationMCPServer {
  private server: express.Application;
  private contextManager: ContextManager;
  private toolRegistry: ToolRegistry;
  
  constructor() {
    this.server = express();
    this.server.use(express.json());
    
    // Initialize MCP components
    this.contextManager = new ContextManager();
    this.toolRegistry = new ToolRegistry();
    
    // Register tools/functions
    this.registerTools();
    
    // Setup routes
    this.setupRoutes();
  }
  
  private registerTools() {
    // Register the external API endpoint as a tool
    this.toolRegistry.register('executeApiCall', async (jsonData: any) => {
      // Logic to call your existing API endpoint
      try {
        const response = await fetch('https://your-api-endpoint.com/action', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonData)
        });
        
        return await response.json();
      } catch (error) {
        return { error: error.message };
      }
    });
  }
  
  private setupRoutes() {
    // Main endpoint for processing natural language inputs
    this.server.post('/api/process', async (req, res) => {
      try {
        const { text, sessionId } = req.body;
        
        if (!text) {
          return res.status(400).json({ error: 'Text input is required' });
        }
        
        // Get or create context for this session
        const context = this.contextManager.getContext(sessionId);
        
        // Process the request using MCP pattern
        const result = await this.processWithMCP(text, context);
        
        // Update context with this interaction
        this.contextManager.updateContext(sessionId, {
          lastInput: text,
          lastOutput: result,
          timestamp: new Date()
        });
        
        res.json(result);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });
  }
  
  private async processWithMCP(text: string, context: any) {
    // 1. Generate structured JSON from natural language using OpenAI
    const structuredData = await this.generateStructuredJson(text, context);
    
    // 2. Validate the generated JSON
    const validatedData = this.validateJson(structuredData);
    
    // 3. Execute the appropriate tool/function with the structured data
    const toolName = this.determineToolFromJson(validatedData);
    const tool = this.toolRegistry.getTool(toolName);
    
    if (!tool) {
      return { error: `Tool '${toolName}' not found` };
    }
    
    // 4. Execute the tool with the structured data
    return await tool(validatedData);
  }
  
  private async generateStructuredJson(text: string, context: any) {
    // Use OpenAI to convert natural language to structured JSON
    const response = await openai.chat.completions.create({
      model: "gpt-4",  // or your preferred model
      messages: [
        {
          role: "system",
          content: `You translate user text into structured JSON for API calls. 
                    Format the JSON according to these specifications: 
                    [Include your API's JSON schema here]
                    
                    Context from previous interactions:
                    ${JSON.stringify(context)}`
        },
        { role: "user", content: text }
      ],
      response_format: { type: "json_object" }
    });
    
    const jsonString = response.choices[0].message.content;
    return JSON.parse(jsonString);
  }
  
  private validateJson(json: any) {
    // Implement validation logic here
    // This could be schema validation using libraries like Joi, Zod, etc.
    return json;
  }
  
  private determineToolFromJson(json: any) {
    // Logic to determine which tool to use based on the JSON content
    // For now, we'll always use the executeApiCall tool
    return 'executeApiCall';
  }
  
  public start(port: number) {
    this.server.listen(port, () => {
      console.log(`MCP Server is running on port ${port}`);
    });
  }
}

// MCP Components
class ContextManager {
  private contexts: Map<string, any> = new Map();
  
  getContext(sessionId: string) {
    if (!sessionId) {
      return {};
    }
    
    if (!this.contexts.has(sessionId)) {
      this.contexts.set(sessionId, {});
    }
    
    return this.contexts.get(sessionId);
  }
  
  updateContext(sessionId: string, contextUpdate: any) {
    const currentContext = this.getContext(sessionId);
    this.contexts.set(sessionId, { ...currentContext, ...contextUpdate });
  }
}

class ToolRegistry {
  private tools: Map<string, Function> = new Map();
  
  register(name: string, handler: Function) {
    this.tools.set(name, handler);
  }
  
  getTool(name: string) {
    return this.tools.get(name);
  }
  
  listTools() {
    return Array.from(this.tools.keys());
  }
}

// Create and start the server
const mcpServer = new ApplicationMCPServer();
mcpServer.start(3000);
