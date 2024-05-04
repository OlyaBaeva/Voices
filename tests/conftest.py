import pytest
from api import create_app


@pytest.fixture
def server():
    app = create_app()
    with app.test_client() as server:
        yield server
