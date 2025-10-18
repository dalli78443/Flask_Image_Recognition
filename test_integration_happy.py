# test_integration_happy.py
"""Integration tests for happy path image upload and prediction."""

from io import BytesIO

def simulate_image_upload(client, image_bytes, filename="test_image.jpg"):
    """Helper to simulate an image upload to the /prediction endpoint."""
    img_data = BytesIO(image_bytes)
    img_data.name = filename
    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )
    return response

def test_successful_prediction(client):
    """Check that a valid image upload returns a prediction."""
    response = simulate_image_upload(client, b"fake_image_data", "test.jpg")
    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_multiple_sequential_predictions(client):
    """Ensure multiple sequential uploads in a single session succeed."""
    filenames = ["img1.jpg", "img2.jpg", "img3.jpg"]
    for name in filenames:
        img_data = BytesIO(b"valid_image_data")
        img_data.name = name
        response = client.post(
            "/prediction",
            data={"file": (img_data, img_data.name)},
            content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert b"Prediction" in response.data
