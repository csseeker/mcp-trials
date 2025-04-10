import requests
import sys  
import os  
import subprocess
from mcp.server.fastmcp import FastMCP  

#mcp = FastMCP("terminal")  
DEFAULT_WORKSPACE = "D:\\repos\\py\\mcp\\workspace"
print(DEFAULT_WORKSPACE)

mcp = FastMCP("ask_planful", workspace=DEFAULT_WORKSPACE)  

config = {
    "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJlbnZUZW5hbnRJZGVudGlmaWVyIjoicGNyZGV2LUJvdERlbW9fSW50ZXJuYWwiLCJjbGllbnRUeXBlIjoiTmF0aXZlIiwiZXhwIjoxNzQ0MzE5Mjc5LCJpYXQiOjE3NDQzMTU2Nzl9.Yo-kjRfDBs8IfBoSrHjDjfDmuBkV3IeL3N6NUviIjP8Olppm1PmftgxwDDvG-xgroBkcIbfW_75WQcMnzU-27OZBJlHt11J1l6-_I1vBZxwk8F7rXxjxNAvNi4iQ_pj0gyr4zWN1u0VPSYpAfPliVaCeRInSK4a1MXq8MWUynLYtScNPr8xwNsr0RN2nq9SxpUengSQH2WmGQ1j7Dk2t8KCzMdx07IV6qixwJZGR7cxiDg4xMIO-QaFnmlU3KDLItnqujkWbXO7o8NthlJqZGYvjihsV6ob53Kryj95n6cV-rIWNy3dhLUplYQecXFUdOE6vJLLQd09ke2CoFz1TLw",
    "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJleHAiOjE3NTk3NDI1OTYsImlhdCI6MTc0NDE5MDU5Nn0.tE12U0GXKVgdv-Ya0lV5tSNJ7dw7oWQbb1WHOp9RFke9jEKwKvukZEQAvctTJ-tak7FJnUz1rIzhMF76rxwidvn1plWKL-zbXGKBUs0neE98-GKHedNs9P_Yzp3Sblih69RVCQELZTlc0Cw7Y3kdLM2ovORJ1s55Vp1oM__dYnwWOSma1X9qfrxwtmaY8wD9LaTL1WUhZq5GnfQP_U9HytILJ_mKoDq8Ujw-EFGy4WIrmeEKaZnQQqERtgQEctly5P8TizWnErPfM8Exqcf5LaqlW6jFXD2gNPwsNXVx1J4yhXgjgVz8-yV-8C2Z1GOCHBPYd6TKGhW01Q_mU6JVWQ",
    "sessionId": "2vYIezeOw1GXCVVII7ZmK5IwOhg",
    "expires_in": 3600,
    "token_type": "bearer",
    "botservice_url": "https://bot.devusai.planful.com/",
    "expires_at_utc": "2025-04-10T21:07:59.8926471Z"
}

# @mcp.tool()  
# async def run_command(command: str):  
#     """  
#     Run a terminal command inside the workspace directory.  
#     """  
#     try:  
#         result = subprocess.run(command, shell=True, cwd=DEFAULT_WORKSPACE, capture_output=True, text=True)  
#         return result.stdout or result.stderr  
#     except Exception as e:  
#         return str(e)

@mcp.tool()  
async def ask_planful(user_query: str):  
    try:
        headers = {
            "Authorization": f"Bearer {config['access_token']}",
            "Content-Type": "application/json",
            "client_type": "mcp_client"
        }
        payload = {
            "command": user_query
        }
        result = requests.post(f"{config['botservice_url']}execute", json=payload, headers=headers)
        #return response.json() if response.status_code == 200 else response.text
        return result.stdout or result.stderr  
    except Exception as e:
        print(str(e), file=sys.stderr)
        return str(e)
    
if __name__ == "__main__":  
    mcp.run(transport='stdio')
