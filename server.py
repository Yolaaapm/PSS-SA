from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Tentukan status code & data berdasarkan endpoint
        if self.path == "/hello":
            status_code = 200
            data = {"message": "Hello from backend"}
        elif self.path == "/students":
            status_code = 200
            data = {"students": ["Fiola", "Ahmad", "Budi"]}
        elif self.path == "/courses":
            status_code = 200
            data = {"courses": ["Pemrograman Sisi Server", "Basis Data"]}
        elif self.path == "/health":
            status_code = 200
            data = {"status": "OK", "uptime": "healthy"}
        else:
            status_code = 404
            data = {"error": "Not found"}

        # 2. KIRIM STATUS RESPONSE TERLEBIH DAHULU (PENTING!)
        self.send_response(status_code)

        # 3. Kirim Header Content-Type
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # 4. Kirim Body Response
        self.wfile.write(json.dumps(data).encode())


server = HTTPServer(("localhost", 8000), Handler)
print("Server running at http://localhost:8000")
server.serve_forever()