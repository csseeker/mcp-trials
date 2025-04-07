import os  
import subprocess  
from mcp.server.fastmcp import FastMCP  

mcp = FastMCP("terminal")  
DEFAULT_WORKSPACE = "D:\\repos\\py\\mcp\\workspace"
print(DEFAULT_WORKSPACE)

@mcp.tool()  
async def run_command(command: str):  
    """  
    Run a terminal command inside the workspace directory.  
    """  
    try:  
        result = subprocess.run(command, shell=True, cwd=DEFAULT_WORKSPACE, capture_output=True, text=True)  
        return result.stdout or result.stderr  
    except Exception as e:  
        return str(e)
    
if __name__ == "__main__":  
    mcp.run(transport='stdio')
