import httpx
from typing import Optional, Dict, Any


class VerdantlyClientAsync:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        if not api_key:
            raise ValueError("API key is required to initialize VerdantlyClient")

        self.api_key = api_key
        self.base_url = base_url or "https://verdantly-gardening-api.p.rapidapi.com"
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "verdantly-gardening-api.p.rapidapi.com"
        }
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)

    async def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None):
        url = f"{self.base_url}{endpoint}"
        response = await self.client.request(method, url, params=params, json=data)

        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        return response.json()

    async def get_plant_variety_categories(self):
        return await self._request("GET", "/v1/plants/varieties/categories")

    async def get_types_by_category(self, category: str):
        return await self._request("GET", f"/v1/plants/varieties/types/{category}")

    async def get_subtypes_by_type(self, type: str):
        return await self._request("GET", f"/v1/plants/varieties/subtypes/{type}")


    async def search_plant_varieties_by_name(self, query: str, page: int = 1):
        return await self._request("GET", "/v1/plants/varieties/name", params={"q": query, "page": page})

    async def search_plant_varieties_by_filter(self, filters: Dict[str, Any], page: int = 1):
        return await self._request("GET", "/v1/plants/varieties/filter", params={**filters, "page": page})

    async def search_plant_species_by_name(self, query: str, page: int = 1):
        return await self._request("GET", "/v1/plants/species/name", params={"q": query, "page": page})

    async def search_plant_species_by_filter(self, filters: Dict[str, Any], page: int = 1):
        return await self._request("GET", "/v1/plants/species/filter", params={**filters, "page": page})

    async def close(self):
        await self.client.aclose()