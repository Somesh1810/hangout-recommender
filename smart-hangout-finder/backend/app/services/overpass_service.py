import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_places(
    lat: float,
    lon: float,
    radius: int = 3000
):

    query = f"""
    [out:json][timeout:25];

    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["amenity"="cafe"](around:{radius},{lat},{lon});
      node["amenity"="fast_food"](around:{radius},{lat},{lon});
      node["amenity"="bar"](around:{radius},{lat},{lon});
    );

    out body;
    """

    try:

        response = requests.get(
            OVERPASS_URL,
            params={"data": query},
            timeout=60,
            headers={
                "User-Agent": "SmartHangoutFinder/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        places = []

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            places.append({
                "name": tags.get("name", "Unknown"),
                "type": tags.get("amenity", ""),
                "lat": item.get("lat"),
                "lon": item.get("lon"),
                "cuisine": tags.get("cuisine", "Unknown")
            })

        return {
            "count": len(places),
            "places": places
        }

    except Exception as e:

        return {
            "error": str(e)
        }