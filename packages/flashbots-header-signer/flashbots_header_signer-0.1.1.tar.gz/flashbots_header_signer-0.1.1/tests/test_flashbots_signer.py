# test_flashbots_signer.py

from http.client import responses
import json
import pytest
from flashbots_header_signer import FlashbotsHeaderSigner
from contextlib import nullcontext as does_not_raise
from aioresponses import aioresponses

from unittest.mock import patch
from conftest import (
    private_key_true,
    tx_body_true,
    headers_true,
    url_test,
    mock_post_response_success,
    mock_response_error_400,
    mock_response_error_403,
    mock_response_error_502
)
from mocks import (
    mock_post_request_success,
    mock_post_request_error_400,
    mock_post_request_error_403,
    mock_post_request_error_502
)

@pytest.mark.parametrize("private_key, expected",  [
    (None, pytest.raises(ValueError)), 
    ("", pytest.raises(ValueError)),
    ("invalid_private_key", pytest.raises(ValueError)),
    (private_key_true, does_not_raise())
])
def test_init_private_key(private_key, expected):
    with expected:
        signer = FlashbotsHeaderSigner(private_key=private_key)
        if private_key:
            assert isinstance(signer, FlashbotsHeaderSigner)


@pytest.mark.parametrize("private_key, log_level, expected",  [
    (private_key_true, None, pytest.raises(ValueError)), 
    (private_key_true, "", pytest.raises(ValueError)),
    (private_key_true, "NOT_A_VALID_LOG_LEVEL", pytest.raises(ValueError)),
    (private_key_true, "CRITICAL", does_not_raise()),
    (private_key_true, "WARNING", does_not_raise()),
    (private_key_true, "ERROR", does_not_raise()),
    (private_key_true, "DEBUG", does_not_raise()),
    (private_key_true, "INFO", does_not_raise()),
])
def test_init_log_level(private_key, log_level, expected):
    with expected:
        signer = FlashbotsHeaderSigner(private_key=private_key, log_level=log_level)
        if private_key:
            assert isinstance(signer, FlashbotsHeaderSigner)


@pytest.mark.parametrize("tx_body, expected",  [
    (None, pytest.raises(ValueError)), 
    ("", pytest.raises(ValueError)),
    ({}, pytest.raises(TypeError)),
    ({"key1": 1 , "key2": "value_2"}, pytest.raises(TypeError)),
    ({"key1": "1" , "key2": "value_2"}, pytest.raises(TypeError)),
    (tx_body_true, does_not_raise()),
])
def test_generate_flashbots_header(tx_body, expected):
    with expected:
        signer = FlashbotsHeaderSigner(private_key=private_key_true)
        headers_json = signer.generate_flashbots_header(tx_body)
        print(headers_json)
                # Assert that the headers_json is a dictionary
        assert isinstance(headers_json, dict)

        # Assert that it contains the expected keys
        assert "Content-Type" in headers_json
        assert "X-Flashbots-Signature" in headers_json

        # Optionally, check if the signature is valid or matches expected format
        assert isinstance(headers_json["X-Flashbots-Signature"], str)
        assert headers_json["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_send_request_success():
    # Set the URL and check headers
    url = url_test
    if isinstance(headers_true, str):
        headers_json = json.loads(headers_true)  # Convert string headers to JSON if needed
    else:
        headers_json = headers_true

    # Use aioresponses to mock the POST request
    with aioresponses() as m:
        m.post(url, payload=mock_post_response_success)

        # Create an instance of the class to send the request
        signer = FlashbotsHeaderSigner(private_key=private_key_true, log_level="DEBUG")
        
        # Send the request and get the response
        response = await signer.send_request(url, headers_json, tx_body_true)

        # If the response is in string format, parse it to JSON
        if isinstance(response, str):
            response_json = json.loads(response)
        else:
            response_json = response

        # Verify that the response is not empty and matches the expected values
        assert response_json is not None
        assert response_json["jsonrpc"] == "2.0"
        assert response_json["id"] == 1
        assert "result" in response_json
        assert response_json["result"]["bundleHash"] == "0x9000000000000000000000000000000000000000000000000000000000000009"


@pytest.mark.asyncio
async def test_send_request_error_400():
    """Test a failed Flashbots API request due to an API error (400 Bad Request)."""
    # Set the URL and check headers
    url = url_test
    if isinstance(headers_true, str):
        headers_json = json.loads(headers_true)  # Convert string headers to JSON if needed
    else:
        headers_json = headers_true

    # Use aioresponses to mock the POST request
    with aioresponses() as m:
        m.post(url, payload=mock_response_error_400, status=400)

        # Create an instance of the class to send the request
        signer = FlashbotsHeaderSigner(private_key=private_key_true, log_level="DEBUG")
        
        # Send the request and get the response
        response = await signer.send_request(url, headers_json, tx_body_true)

        # If the response is in string format, parse it to JSON
        if isinstance(response, str):
            response_json = json.loads(response)
        else:
            response_json = response
        print(response)
        print(response_json)
        
        # Check if response_json is None
        assert response_json is not None

        # Verify that the response contains the expected error message
        assert "error" in response_json
        assert response_json["error"]["message"] == "Invalid transaction"


@pytest.mark.asyncio
async def test_send_request_error_403():
    """Test a failed Flashbots API request due to an API error (400 Bad Request)."""
    # Set the URL and check headers
    url = url_test
    if isinstance(headers_true, str):
        headers_json = json.loads(headers_true)  # Convert string headers to JSON if needed
    else:
        headers_json = headers_true

    # Use aioresponses to mock the POST request
    with aioresponses() as m:
        m.post(url, payload=mock_response_error_403, status=403)

        # Create an instance of the class to send the request
        signer = FlashbotsHeaderSigner(private_key=private_key_true, log_level="DEBUG")
        
        # Send the request and get the response
        response = await signer.send_request(url, headers_json, tx_body_true)

        # If the response is in string format, parse it to JSON
        if isinstance(response, str):
            response_json = json.loads(response)
        else:
            response_json = response
            
        print(response)
        print(response_json)
        print(type(response_json))

        # Check if response_json is None
        assert response_json is not None

        # Verify that the response contains the expected error message
        assert "error" in response_json
        assert response_json["error"]["message"] == "Forbidden access"


@pytest.mark.asyncio
async def test_send_request_error_502():
    """Test a failed Flashbots API request due to an API error (400 Bad Request)."""
    # Set the URL and check headers
    url = url_test
    if isinstance(headers_true, str):
        headers_json = json.loads(headers_true)  # Convert string headers to JSON if needed
    else:
        headers_json = headers_true

    # Use aioresponses to mock the POST request
    with aioresponses() as m:
        m.post(url, payload=mock_response_error_502, status=502)

        # Create an instance of the class to send the request
        signer = FlashbotsHeaderSigner(private_key=private_key_true, log_level="DEBUG")
        
        # Send the request and get the response
        response = await signer.send_request(url, headers_json, tx_body_true)

        # If the response is in string format, parse it to JSON
        if isinstance(response, str):
            response_json = json.loads(response)
        else:
            response_json = response
            
        print(response)
        print(response_json)
        print(type(response_json))

        # Check if response_json is None
        assert response_json is not None

        # Verify that the response contains the expected error message
        assert "error" in response_json
        assert response_json["error"]["message"] == "Bad gateway error"


@pytest.mark.asyncio
async def test_send_request_invalid_url():
    """Test method call with an invalid URL."""
    
    signer = FlashbotsHeaderSigner(private_key=private_key_true)

    # Check that a TypeError is raised when an invalid URL is passed
    with pytest.raises(TypeError, match="url must be a string"):
        await signer.send_request(12345, {}, "{}")  # URL is passed as a number, not a string

@pytest.mark.asyncio
async def test_send_request_invalid_headers():
    """Test method call with invalid headers."""
    
    signer = FlashbotsHeaderSigner(private_key=private_key_true)

    with pytest.raises(TypeError):
        await signer.send_request(url_test, None, "{}")  # headers_json is None

    with pytest.raises(TypeError):
        await signer.send_request(url_test, 123, "{}")  # headers_json is not a dict/str


@pytest.mark.asyncio
async def test_send_request_invalid_tx_body():
    """Test method call with an invalid transaction body."""
    
    signer = FlashbotsHeaderSigner(private_key=private_key_true)

    with pytest.raises(TypeError):
        await signer.send_request(url_test, {}, 123)  # tx_body is not a string

    with pytest.raises(json.JSONDecodeError):
        await signer.send_request(url_test, "{}", "invalid json")  # Invalid JSON in tx_body
