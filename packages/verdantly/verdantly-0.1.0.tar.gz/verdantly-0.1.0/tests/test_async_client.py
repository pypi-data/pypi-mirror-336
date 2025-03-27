import pytest
import httpx
from httpx import Response
from unittest.mock import patch
from verdantly_client_async import VerdantlyClientAsync

API_KEY = "test-key"

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_get_plant_variety_categories(mock_request):
    mock_request.return_value = Response(200, json={"data": ["fruit"]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.get_plant_variety_categories()
    assert result == {"data": ["fruit"]}
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_get_types_by_category(mock_request):
    mock_request.return_value = Response(200, json={"data": ["apple"]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.get_types_by_category("fruit")
    assert result == {"data": ["apple"]}
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_get_subtypes_by_type(mock_request):
    mock_request.return_value = Response(200, json={"data": ["crabapple"]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.get_subtypes_by_type("apple")
    assert result == {"data": ["crabapple"]}
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_search_plant_varieties_by_name(mock_request):
    mock_request.return_value = Response(200, json={"data": [{"name": "basil"}]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.search_plant_varieties_by_name("basil")
    assert result["data"][0]["name"] == "basil"
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_search_plant_varieties_by_filter(mock_request):
    mock_request.return_value = Response(200, json={"data": [{"name": "oregano"}]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.search_plant_varieties_by_filter({"category": "herb"})
    assert result["data"][0]["name"] == "oregano"
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_search_plant_species_by_name(mock_request):
    mock_request.return_value = Response(200, json={"data": [{"name": "Hypericum calycinum"}]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.search_plant_species_by_name("hypericum")
    assert result["data"][0]["name"] == "Hypericum calycinum"
    await client.close()

@pytest.mark.asyncio
@patch("verdantly_client_async.httpx.AsyncClient.request")
async def test_search_plant_species_by_filter(mock_request):
    mock_request.return_value = Response(200, json={"data": [{"name": "Thermopsis villosa"}]})
    client = VerdantlyClientAsync(api_key=API_KEY)
    result = await client.search_plant_species_by_filter({"category": "Dicot"})
    assert result["data"][0]["name"] == "Thermopsis villosa"
    await client.close()
