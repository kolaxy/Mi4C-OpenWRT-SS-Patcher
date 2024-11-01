import socketserver
import threading
import time
import sys


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        filename = self.rfile.readline().strip().decode('UTF-8')
        print("Local file server is getting '{}' for {}.".format(filename, self.client_address[0]))
        try:
            with open("{}/{}".format(self.server.root_dir, filename), "rb") as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"HTTP/1.1 404 Not Found\r\n\r\nFile not found.")
        except Exception as e:
            print(f"Error: {e}")
            self.wfile.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer error.")
        finally:
            self.wfile.close()


class TcpFileServer:
    def __init__(self, root_dir='.'):
        HOST, PORT = '', 0
        self.server = socketserver.TCPServer((HOST, PORT), RequestHandler)
        self.server.root_dir = root_dir
        self.ip, self.port = self.server.server_address

    def __enter__(self):
        self.run()
        return self

    def run(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print("Local file server is running on {}:{}. Root='{}'".format(self.ip, self.port, self.server.root_dir))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.shutdown()
        self.server.server_close()


if __name__ == "__main__":
    root_dir = '.' if len(sys.argv) <= 1 else sys.argv[1]
    with TcpFileServer(root_dir):
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("Server is shutting down...")
