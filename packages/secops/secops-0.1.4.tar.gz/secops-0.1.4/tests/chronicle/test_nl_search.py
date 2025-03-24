# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Unit tests for natural language search functionality."""

import pytest
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from secops.chronicle.nl_search import translate_nl_to_udm, nl_search
from secops.exceptions import APIError

@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = MagicMock()
    client.region = "us"
    client.project_id = "test-project"
    client.customer_id = "test-customer-id"
    
    # Mock session with response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"query": "ip != \"\""}
    client.session.post.return_value = mock_response
    
    return client

def test_translate_nl_to_udm_success(mock_client):
    """Test successful translation of natural language to UDM."""
    result = translate_nl_to_udm(mock_client, "show me ip addresses")
    
    # Verify the request was made with correct parameters
    mock_client.session.post.assert_called_once()
    call_args = mock_client.session.post.call_args
    
    # Check URL format
    url = call_args[0][0]
    assert "us-chronicle.googleapis.com" in url
    assert "test-project" in url
    assert "test-customer-id" in url
    assert ":translateUdmQuery" in url
    
    # Check payload
    payload = call_args[1]["json"]
    assert payload == {"text": "show me ip addresses"}
    
    # Check result
    assert result == "ip != \"\""

def test_translate_nl_to_udm_error_response(mock_client):
    """Test error response handling in translation."""
    # Set up mock response for error case
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Invalid request"
    mock_client.session.post.return_value = mock_response
    
    # Test error handling
    with pytest.raises(APIError, match="Chronicle API request failed: Invalid request"):
        translate_nl_to_udm(mock_client, "invalid query")

def test_translate_nl_to_udm_no_valid_query(mock_client):
    """Test handling when no valid query can be generated."""
    # Set up mock response for no valid query case
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Sorry, no valid query could be generated. Try asking a different way."
    }
    mock_client.session.post.return_value = mock_response
    
    # Test error handling for no valid query
    with pytest.raises(APIError, match="Sorry, no valid query could be generated"):
        translate_nl_to_udm(mock_client, "nonsensical query")

@patch('secops.chronicle.nl_search.translate_nl_to_udm')
def test_nl_search(mock_translate, mock_client):
    """Test the natural language search function."""
    # Set up mocks
    mock_translate.return_value = "ip != \"\""
    mock_client.search_udm.return_value = {"events": [], "total_events": 0}
    
    # Define test parameters
    start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    end_time = datetime.now(timezone.utc)
    
    # Call the function
    result = nl_search(
        mock_client, 
        "show me ip addresses", 
        start_time, 
        end_time
    )
    
    # Verify translate_nl_to_udm was called
    mock_translate.assert_called_once_with(mock_client, "show me ip addresses")
    
    # Verify search_udm was called with the translated query
    mock_client.search_udm.assert_called_once()
    call_args = mock_client.search_udm.call_args
    assert call_args[1]["query"] == "ip != \"\""
    assert call_args[1]["start_time"] == start_time
    assert call_args[1]["end_time"] == end_time
    
    # Check result
    assert result == {"events": [], "total_events": 0}

@patch('secops.chronicle.nl_search.translate_nl_to_udm')
def test_nl_search_translation_error(mock_translate, mock_client):
    """Test error handling when translation fails."""
    # Set up translation to raise an error
    mock_translate.side_effect = APIError("Sorry, no valid query could be generated")
    
    # Define test parameters
    start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    end_time = datetime.now(timezone.utc)
    
    # Test error handling
    with pytest.raises(APIError, match="Sorry, no valid query could be generated"):
        nl_search(mock_client, "invalid query", start_time, end_time)
    
    # Verify search_udm was not called
    mock_client.search_udm.assert_not_called()

def test_chronicle_client_integration():
    """Test that ChronicleClient correctly exposes the methods."""
    # This is a structural test, not a functional test
    # It ensures that the methods are correctly exposed on the client
    
    from secops.chronicle import ChronicleClient
    from secops.chronicle.client import ChronicleClient as DirectClient
    
    # Get method references
    client_method = getattr(DirectClient, "translate_nl_to_udm", None)
    search_method = getattr(DirectClient, "nl_search", None)
    
    # Check that methods exist on the client
    assert client_method is not None, "translate_nl_to_udm method not found on ChronicleClient"
    assert search_method is not None, "nl_search method not found on ChronicleClient"
    
    # Additional check from the module import
    assert hasattr(ChronicleClient, "translate_nl_to_udm")
    assert hasattr(ChronicleClient, "nl_search") 