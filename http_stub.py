# http_stub.py — serveur HTTP ultra simple pour Render gratuit
import os, socket, threading

def serve():
    port = int(os.environ.get("PORT", "10000"))
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    while True:
        conn, _ = s.accept()
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBot is running")
        conn.close()

def start_http_stub():
    threading.Thread(target=serve, daemon=True).start()
