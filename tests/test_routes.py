from app import app

def test_home_page_loads():
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_scanner_page_loads():
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/scanner")
        assert response.status_code == 200
