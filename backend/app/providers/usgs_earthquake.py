import math
import httpx


USGS_4_5_WEEK_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


async def get_nearby_earthquakes(latitude: float, longitude: float, radius_km: int = 800) -> list[dict]:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(USGS_4_5_WEEK_URL)
        response.raise_for_status()
        data = response.json()

    nearby = []

    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        if len(coordinates) < 2:
            continue

        quake_lon = coordinates[0]
        quake_lat = coordinates[1]
        quake_depth = coordinates[2] if len(coordinates) > 2 else None

        distance = distance_km(latitude, longitude, quake_lat, quake_lon)

        if distance <= radius_km:
            nearby.append(
                {
                    "title": properties.get("title"),
                    "place": properties.get("place"),
                    "magnitude": properties.get("mag"),
                    "url": properties.get("url"),
                    "time": properties.get("time"),
                    "distance_km": round(distance, 1),
                    "depth_km": quake_depth,
                }
            )

    nearby.sort(key=lambda item: item["distance_km"])

    return nearby[:5]
