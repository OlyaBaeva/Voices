import pytest
import threading
from flask.testing import FlaskCliRunner
from api import app


@pytest.fixture
def app_server():
    runner = FlaskCliRunner(app)
    process = threading.Thread(target=runner.invoke, args=["run", "--no-reloader"])
    process.start()

    yield
    process.join()
