from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/orders/"):
            self._send(200, {"order_id": self.path.split("/")[-1], "item": "shoes"})
        elif self.path.startswith("/api/billing/"):
            self._send(200, {"billing_id": self.path.split("/")[-1], "card": "XXXX"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        self._send(201, {"status": "created"})

print("Mock server running on port 8080")
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
