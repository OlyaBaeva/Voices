from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class MockServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = '{"temperature": 20}'
        self.wfile.write(response.encode())


class MockServer:
    def __init__(self):
        self.server = None
        self.stop_event = threading.Event()

    def start(self):
        server_address = ('адрес мок-сервера', 8000)
        self.server = HTTPServer(server_address, MockServerHandler)
        print('Mock server started on port 8000')
        while not self.stop_event.is_set():
            self.server.handle_request()


def run_mock_server():
    global mock_server
    mock_server = MockServer()
    mock_server.start()


if __name__ == '__main__':
    run_mock_server()
