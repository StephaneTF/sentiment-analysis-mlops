from app import app

client = app.test_client()


def test_predict_returns_positive_sentiment():
    response = client.post(
        "/predict",
        json={"tweet": "I absolutely love this!"},
    )

    assert response.status_code == 200
    assert response.get_json()["sentiment"] == "positive"


def test_predict_rejects_missing_tweet():
    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()