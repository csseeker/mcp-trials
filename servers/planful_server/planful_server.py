import requests
import sys  
import os  
import subprocess
from mcp.server.fastmcp import FastMCP  
import asyncio

#mcp = FastMCP("terminal")  
DEFAULT_WORKSPACE = "D:\\repos\\py\\mcp\\workspace"
print(DEFAULT_WORKSPACE)

mcp = FastMCP("ask_planful")  

config = {
    "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJlbnZUZW5hbnRJZGVudGlmaWVyIjoicGNyZGV2LUJvdERlbW9fSW50ZXJuYWwiLCJjbGllbnRUeXBlIjoiTmF0aXZlIiwiZXhwIjoxNzQ0NDUzMzQ1LCJpYXQiOjE3NDQ0NDk3NDV9.sedFVaQr20lx03h5A92uqtqQlieM6CGI2XA_2RjCrE_pe6lQpECDxYiXM9VGMjQH0i1vxZO5ZwOKOn12yGU1MZw7WMKUMPkcG0EsqnQowQvkHYGLw8vAA3-qjmzXQDbxBhEp4DttURsA5WGjU8Ig347ydC6U1cx66JQfqwFG8bTOEjJ9QtVTSvK7G5HaAIqGqAE860WdGNidk27GAJQeMj_CnNhLsFNCUYyada24rdk3IPz7WJB_Zti3_xUbI2lC8be6h8jU0E1SUU-TsEG_CAMbOL2IV05GrbhhC08hESLAFjM_zKF5W_s2N2ax-h4mMZTgeAwkbGq70yLkjU5LfA",
    "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIydlVEODduM0xIUkFVVTIxRDM2bVlQZUJSTWgiLCJleHAiOjE3NTk3NDI1OTYsImlhdCI6MTc0NDE5MDU5Nn0.tE12U0GXKVgdv-Ya0lV5tSNJ7dw7oWQbb1WHOp9RFke9jEKwKvukZEQAvctTJ-tak7FJnUz1rIzhMF76rxwidvn1plWKL-zbXGKBUs0neE98-GKHedNs9P_Yzp3Sblih69RVCQELZTlc0Cw7Y3kdLM2ovORJ1s55Vp1oM__dYnwWOSma1X9qfrxwtmaY8wD9LaTL1WUhZq5GnfQP_U9HytILJ_mKoDq8Ujw-EFGy4WIrmeEKaZnQQqERtgQEctly5P8TizWnErPfM8Exqcf5LaqlW6jFXD2gNPwsNXVx1J4yhXgjgVz8-yV-8C2Z1GOCHBPYd6TKGhW01Q_mU6JVWQ",
    "sessionId": "2vcgOfhqbx46DI9ars0a7yFevOp",
    "expires_in": 3600,
    "token_type": "bearer",
    "botservice_url": "https://bot.devusai.planful.com/",
    "expires_at_utc": "2025-04-12T10:22:25.396525Z"
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
            "messageContext": {
            "sessionId": config["sessionId"],
            "conversationId": "",
            "mode": "Analyze",
            "messageId": ""
            },
            "source": "NL",
            "sourceContext": {
            "userInput": user_query
            }
        }
        url=f"{config['botservice_url']}chat/ask"
        #print(f" --- URL --- : {url}", file=sys.stdout)
        #print(f" --- Payload --- : {payload}", file=sys.stdout)

        response = requests.post(url, json=payload, headers=headers)
        result = response.json() if response.status_code == 200 else response.text
        #print(f" --- Response --- : {result}", file=sys.stdout)
        return result
        #return result.stdout or result.stderr  
    except Exception as e:
        print(str(e), file=sys.stderr)
        return str(e)
    
if __name__ == "__main__":  
    # res = asyncio.run(ask_planful("What is the revenue for 2022?"))
    # print(res)
    print("Starting Planful Server...")
    mcp.run(transport='stdio')
    print("Planful Server Ended.")
