import pytest
from mock_server import run_mock_server


@pytest.fixture
def mock_server():
    import threading
    server_thread = threading.Thread(target=run_mock_server)
    server_thread.start()
    print("Mock server started")
    yield
    print("Mock server stopped")
    server_thread.join()
    print("Test passed")