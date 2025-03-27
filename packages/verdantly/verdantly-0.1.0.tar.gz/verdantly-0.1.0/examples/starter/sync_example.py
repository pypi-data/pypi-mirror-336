from verdantly_client import VerdantlyClient

RAPID_API_KEY = "<YOUR_RAPID_API_KEY>"

def find_low_water_fruit_trees():
    print("Searching for fruit trees with low water needs...\n")

    client = VerdantlyClient(api_key=RAPID_API_KEY)
    results = client.search_plant_varieties_by_filter({
        "category": "fruit",
        "waterRequirement": "low"
    })

    if not results.get("data"):
        print("No fruit trees found with low water requirement.")
        return

    for plant in results["data"]:
        print(f"\U0001F333 {plant.get('name')}")
        growing = plant.get("growingRequirements", {})
        print(f"   Water: {growing.get('waterRequirement')}")
        print(f"   Zone: {growing.get('growingZoneRange')}")
        print(f"   Highlights: {plant.get('highlights')}")
        print(f"   History: {plant.get('history')}\n")

if __name__ == "__main__":
    find_low_water_fruit_trees()