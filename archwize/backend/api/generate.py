from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add the parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import DiagramService

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data.decode('utf-8'))
        
        # Set CORS headers for pre-flight requests
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Extract parameters
            prompt = request_data.get('prompt', '')
            orientation = request_data.get('orientation', 'TD')
            
            if not prompt:
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'missing_prompt',
                    'message': 'Prompt is required'
                }).encode())
                return
            
            # Generate the diagram
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            mermaid_code = loop.run_until_complete(
                DiagramService.generate_mermaid_diagram(prompt, orientation)
            )
            
            # Return the response
            self.wfile.write(json.dumps({
                'success': True,
                'mermaid_code': mermaid_code,
                'message': 'Diagram generated successfully'
            }).encode())
            
        except Exception as e:
            # Handle errors
            error_message = str(e)
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'generation_error',
                'message': f'Error generating diagram: {error_message}'
            }).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 