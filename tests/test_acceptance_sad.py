# test_acceptance_sad.py

import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture for the Flask test client.
    - Purpose: Set up a test client for making requests to the Flask app during testing.
    - Usage: Provides a `client` object to use for HTTP request simulations.
    """
    with app.test_client() as client:
        yield client

def test_acceptance_missing_file(client):
    """
    Test Case: No File Uploaded
    - Purpose: Validate the application's behavior when no file is provided in the upload request.
    - Scenario:
        - Simulate a POST request to the `/prediction` route with no file data.
        - Assert the response status code is 200 (to indicate a valid request was processed).
        - Verify that the response includes an appropriate error message.
    """
    # Simulate a POST request with no file data
    response = client.post("/prediction", data={}, content_type="multipart/form-data")

    # Assertions:
    # 1. Ensure the response status code is 200, indicating the request was processed.
    assert response.status_code == 200

    # 2. Check for a meaningful error message in the response data.
    #    Modify the message check if your application uses a different error response text.
    assert b"File cannot be processed" in response.data  # Expected error message

#additional
def test_acceptance_invalid_file_type(client):
    """
    Test Case: Invalid File Type Uploaded
    - Purpose: Validate the application's behavior when a non-image file is uploaded.
    - Scenario:
        - Simulate a POST request to the `/prediction` route with a text file or corrupted data.
        - Assert the response status code is 200 (request processed).
        - Verify that the response includes an appropriate error message.
    """
    # Simulate uploading a non-image file
    from io import BytesIO
    invalid_file = BytesIO(b"this_is_not_an_image")
    invalid_file.name = "not_an_image.txt"

    response = client.post(
        "/prediction",
        data={"file": (invalid_file, invalid_file.name)},
        content_type="multipart/form-data"
    )

    # Assertions:
    assert response.status_code == 200
    assert b"File cannot be processed" in response.data  # Expected error message
