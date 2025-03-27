import pytest
import requests
from requests.models import Response
from unittest.mock import patch
from verdantly_client import VerdantlyClient

API_KEY = "test-key"

@patch("verdantly_client.requests.request")
def test_get_plant_variety_categories(mock_request):
    mock_request.return_value = MockResponse({"data": ["fruit"]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.get_plant_variety_categories()
    assert result == {"data": ["fruit"]}

@patch("verdantly_client.requests.request")
def test_get_types_by_category(mock_request):
    mock_request.return_value = MockResponse({"data": ["apple"]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.get_types_by_category("fruit")
    assert result == {"data": ["apple"]}

@patch("verdantly_client.requests.request")
def test_get_subtypes_by_type(mock_request):
    mock_request.return_value = MockResponse({"data": ["crabapple"]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.get_subtypes_by_type("apple")
    assert result == {"data": ["crabapple"]}

@patch("verdantly_client.requests.request")
def test_search_plant_varieties_by_name(mock_request):
    mock_request.return_value = MockResponse({"data": [{"name": "basil"}]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.search_plant_varieties_by_name("basil")
    assert result["data"][0]["name"] == "basil"

@patch("verdantly_client.requests.request")
def test_search_plant_varieties_by_filter(mock_request):
    mock_request.return_value = MockResponse({"data": [{"name": "oregano"}]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.search_plant_varieties_by_filter({"category": "herb"})
    assert result["data"][0]["name"] == "oregano"

@patch("verdantly_client.requests.request")
def test_search_plant_species_by_name(mock_request):
    mock_request.return_value = MockResponse({"data": [{"name": "Hypericum calycinum"}]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.search_plant_species_by_name("hypericum")
    assert result["data"][0]["name"] == "Hypericum calycinum"

@patch("verdantly_client.requests.request")
def test_search_plant_species_by_filter(mock_request):
    mock_request.return_value = MockResponse({"data": [{"name": "Thermopsis villosa"}]})
    client = VerdantlyClient(api_key=API_KEY)
    result = client.search_plant_species_by_filter({"category": "Dicot"})
    assert result["data"][0]["name"] == "Thermopsis villosa"


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code
        self.ok = self.status_code == 200
        self.reason = "OK"
        self.text = str(json_data)

    def json(self):
        return self._json_data