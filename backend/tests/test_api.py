"""
Integration tests for the FastAPI endpoints.

These tests use httpx to simulate real HTTP requests to our API.
We mock the Tesseract OCR call to avoid dependency on the external binary.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test that the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

@patch('backend.main.pytesseract.image_to_string')
def test_upload_receipt_success(mock_ocr):
    """Test uploading a dummy image and receiving parsed data."""
    # 1. Configure the mock to return a realistic receipt string
    mock_ocr.return_value = """
    WALMART STORE
    Date: 01/15/2024
    Milk          $3.99
    Bread         $2.49
    Total:        $6.48
    """

    from io import BytesIO
    from PIL import Image
    
    # Create a simple 100x100 white image in memory
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {'file': ('test_receipt.png', img_bytes, 'image/png')}
    
    response = client.post("/upload/", files=files)
    
    # Debugging print
    if response.status_code != 200:
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert data["data"]["merchant"] == "WALMART STORE"
    assert data["data"]["total"] == 6.48