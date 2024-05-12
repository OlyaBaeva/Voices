from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_get_cards():
    """test fastAPI endpoint '/cards/ with username 'Kirill'"""
    response = client.get("/cards/Kirill")
    assert response.status_code == 200
    assert response.json() == {"card_1": {
                "card_number": '1234',
                "balance": "5000"
            },
            "card_2": {
                "card_number": '5678',
                "balance": "1000"
            }
    }
