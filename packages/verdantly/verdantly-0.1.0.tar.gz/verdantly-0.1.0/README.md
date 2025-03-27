# Verdantly Python Client

The official Python client for accessing plant variety and species data from the Verdantly API.

---

## Installation

```bash
pip install verdantly
```

Or install from source:

```bash
pip install -e .
```

---

## Getting Started

You'll need a valid API key from [RapidAPI](https://rapidapi.com/verdantly-team-verdantly-team-default/api/verdantly-gardening-api).

```python
from verdantly_client import VerdantlyClient

client = VerdantlyClient(api_key="your-api-key")
```

---

## Example Usage (Sync)

```python
results = client.search_plant_varieties_by_filter({
  "category": "fruit",
  "waterRequirement": "low"
})

for plant in results["data"]:
  print(plant["name"])
```

---

## Example Usage (Async)

```python
from verdantly_client_async import VerdantlyClientAsync
import asyncio

async def main():
    client = VerdantlyClientAsync(api_key="your-api-key")
    results = await client.search_plant_varieties_by_filter({
        "category": "fruit",
        "waterRequirement": "low"
    })
    for plant in results["data"]:
        print(plant["name"])
    await client.close()

asyncio.run(main())
```

More examples available in [`starter/`](./starter).

---

## Supported Endpoints

- `get_plant_variety_categories()`
- `get_types_by_category(category: str)`
- `get_subtypes_by_type(type: str)`
- `search_plant_varieties_by_name(query: str, page: int = 1)`
- `search_plant_varieties_by_filter(filters: dict, page: int = 1)`
- `search_plant_species_by_name(query: str, page: int = 1)`
- `search_plant_species_by_filter(filters: dict, page: int = 1)`

---

## Project Structure

- `verdantly_client.py` — sync client
- `verdantly_client_async.py` — async client
- `starter/` — runnable starter project with real use case
- `tests/` — test suite for both clients

---

## License

MIT © Verdantly
