from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'message': 'ArchWize Backend API Running!',
            'version': '1.0.0',
            'endpoints': [
                {
                    'path': '/api/generate',
                    'method': 'POST',
                    'description': 'Generate a diagram from a text prompt'
                }
            ]
        }
        
        self.wfile.write(json.dumps(response).encode()) 