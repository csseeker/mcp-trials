import socket
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

class StudioMCPClient:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to the Studio protocol MCP server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            # Studio protocol may require handshake
            self.send_handshake()
            return True, f"Connected to Studio MCP server at {self.host}:{self.port}"
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    def send_handshake(self):
        """Send initial handshake for Studio protocol."""
        handshake = {
            "type": "connect",
            "protocol": "studio",
            "version": "1.0"
        }
        self.socket.sendall(json.dumps(handshake).encode('utf-8') + b'\r\n')
    
    def disconnect(self):
        """Disconnect from the MCP server."""
        if self.socket:
            # Send disconnect message for clean closure
            try:
                disconnect_msg = {"type": "disconnect"}
                self.socket.sendall(json.dumps(disconnect_msg).encode('utf-8') + b'\r\n')
            except:
                pass
            self.socket.close()
            self.socket = None
            self.connected = False
            return "Disconnected from Studio MCP server"
    
    def send_command(self, command_text):
        """Send a command to the Studio MCP server."""
        if not self.socket:
            return "Not connected to server"
        
        try:
            # Format command according to Studio protocol
            command = {
                "type": "command",
                "data": command_text
            }
            
            # Studio protocol typically uses CRLF (\r\n) as line ending
            data = json.dumps(command).encode('utf-8')
            self.socket.sendall(data + b'\r\n')
            
            # Wait for response
            response = self.receive_response()
            return f"Response: {response}"
        except Exception as e:
            return f"Error sending command: {e}"
    
    def receive_response(self):
        """Receive response from the server using Studio protocol."""
        data = b''
        while b'\r\n' not in data:  # Studio typically uses CRLF
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            data += chunk
        
        try:
            response = json.loads(data.decode('utf-8').strip())
            # Extract the actual response data from Studio protocol wrapper
            if isinstance(response, dict) and 'data' in response:
                return response['data']
            return response
        except json.JSONDecodeError:
            return data.decode('utf-8').strip()

class StudioMCPClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Studio MCP Client")
        self.root.geometry("600x500")
        self.client = StudioMCPClient()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Server connection frame
        conn_frame = tk.Frame(self.root, pady=10)
        conn_frame.pack(fill=tk.X)
        
        tk.Label(conn_frame, text="Host:").grid(row=0, column=0, padx=5)
        self.host_entry = tk.Entry(conn_frame, width=15)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(conn_frame, text="Port:").grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(conn_frame, width=6)
        self.port_entry.insert(0, "9000")
        self.port_entry.grid(row=0, column=3, padx=5)
        
        self.conn_button = tk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.conn_button.grid(row=0, column=4, padx=10)
        
        # Command entry
        cmd_frame = tk.Frame(self.root, pady=10)
        cmd_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(cmd_frame, text="Command:").pack(side=tk.LEFT, padx=5)
        self.cmd_entry = tk.Entry(cmd_frame)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.cmd_entry.bind("<Return>", self.send_command)
        
        self.send_button = tk.Button(cmd_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.send_button.config(state=tk.DISABLED)
        
        # Log display
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(log_frame, text="Communication Log:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
    def toggle_connection(self):
        if not self.client.connected:
            host = self.host_entry.get()
            try:
                port = int(self.port_entry.get())
            except ValueError:
                self.log_message("Invalid port number")
                return
                
            self.client = StudioMCPClient(host, port)
            success, message = self.client.connect()
            self.log_message(message)
            
            if success:
                self.conn_button.config(text="Disconnect")
                self.send_button.config(state=tk.NORMAL)
        else:
            message = self.client.disconnect()
            self.log_message(message)
            self.conn_button.config(text="Connect")
            self.send_button.config(state=tk.DISABLED)
    
    def send_command(self, event=None):
        command = self.cmd_entry.get()
        if not command:
            return
            
        self.log_message(f"Sent: {command}")
        
        # Use a thread to avoid blocking the UI
        def send_in_background():
            response = self.client.send_command(command)
            self.log_message(response)
            
        threading.Thread(target=send_in_background).start()
        self.cmd_entry.delete(0, tk.END)
    
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudioMCPClientGUI(root)
    root.mainloop()
    