import requests
import sys  
import os  
import subprocess
from mcp.server.fastmcp import FastMCP  

#mcp = FastMCP("terminal")  
DEFAULT_WORKSPACE = "D:\\repos\\py\\mcp\\workspace"
print(DEFAULT_WORKSPACE)

mcp = FastMCP("ask_planful")  

config = {
    "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJlbnZUZW5hbnRJZGVudGlmaWVyIjoicGNyZGV2LUJvdERlbW9fSW50ZXJuYWwiLCJjbGllbnRUeXBlIjoiTmF0aXZlIiwiZXhwIjoxNzQ0MzI1MTA0LCJpYXQiOjE3NDQzMjE1MDR9.x3JPcJ1Lt7ReJeQVpBBRUcV8HGVWwXioPlGt455MykUJiShcanujZhQq3P37QnLamjzB4SgFD4uWLizObNmN8_8KdoRrFyhEKkWdHdrEG3zB8Vzh_edDDAydbwm6F7-2A1LBlXNNdHz3ygJGJ1BxJdeYCNMXLlgHnCYQn94eX2A3sYTdS8ww5ZvRkjsa61bSLAwc3vMcEryHig_rrQbQGqmrVD54YjDy2Vje23qjJiEcjthadYHQGlFuYywSaadrkOvwrk8tPLsWueZdo5SxOw07AoJN94Mw2DTlM_mtdraeFI2W1ci4r9z8trB4LBdss0CM9AUOfZA7CqO4d1Ht2g",
    "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJleHAiOjE3NTk3NDI1OTYsImlhdCI6MTc0NDE5MDU5Nn0.tE12U0GXKVgdv-Ya0lV5tSNJ7dw7oWQbb1WHOp9RFke9jEKwKvukZEQAvctTJ-tak7FJnUz1rIzhMF76rxwidvn1plWKL-zbXGKBUs0neE98-GKHedNs9P_Yzp3Sblih69RVCQELZTlc0Cw7Y3kdLM2ovORJ1s55Vp1oM__dYnwWOSma1X9qfrxwtmaY8wD9LaTL1WUhZq5GnfQP_U9HytILJ_mKoDq8Ujw-EFGy4WIrmeEKaZnQQqERtgQEctly5P8TizWnErPfM8Exqcf5LaqlW6jFXD2gNPwsNXVx1J4yhXgjgVz8-yV-8C2Z1GOCHBPYd6TKGhW01Q_mU6JVWQ",
    "sessionId": "2vYUT0FuKEtRGN0cE756ho59iHi",
    "expires_in": 3600,
    "token_type": "bearer",
    "botservice_url": "https://bot.devusai.planful.com/",
    "expires_at_utc": "2025-04-10T22:45:04.8591632Z"
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
        response = requests.post(f"{config['botservice_url']}chat/ask", json=payload, headers=headers)
        result = response.json() if response.status_code == 200 else response.text
        print(f" --- Response --- : {result}", file=sys.stdout)
        return result
        #return result.stdout or result.stderr  
    except Exception as e:
        print(str(e), file=sys.stderr)
        return str(e)
    
if __name__ == "__main__":  
    print("Starting Planful Server...")
    mcp.run(transport='stdio')
    print("Planful Server Ended.")
