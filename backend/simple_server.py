import http.server
import socketserver
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Servir archivos desde la carpeta frontend
        frontend_path = Path(__file__).parent.parent / "frontend"
        os.chdir(frontend_path)
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        # Log personalizado
        print(f"🌐 Frontend - {self.address_string()} - {format%args}")

def run_frontend_server():
    PORT = 8080
    frontend_path = Path(__file__).parent.parent / "frontend"
    
    if not frontend_path.exists():
        print(f"❌ Error: No se encuentra la carpeta frontend en {frontend_path}")
        return
    
    os.chdir(frontend_path)
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🌐 Servidor frontend iniciado en http://localhost:{PORT}")
        print(f"📁 Sirviendo archivos desde: {frontend_path}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor frontend detenido")

if __name__ == "__main__":
    run_frontend_server()