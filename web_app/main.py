"""This is my super cool web app"""

import requests
from fastapi import FastAPI, exceptions

app = FastAPI()


@app.get("/")
def root():
    """The root endpoint for the web app"""
    return {"message": "Hello World"}


# Invoke-WebRequest -Method POST "http://localhost:8000/convert/Pennsylvania/Pittsburgh"
@app.post("/convert/{state}/{city}")
def convert(state: str, city: str) -> dict[str, str]:
    """Converts a city, state pair to lat/long"""
    print(f"Converting {city}, {state} to lat/long")
    lat, long = None, None
    api_key = "6a7f57138e04b429290986wxia11d90"
    payload = {"api_key": api_key, "state": state, "city": city}

    try:  # hit other API
        response = requests.get(
            "https://geocode.maps.co/search", params=payload, timeout=2
        )
        response.raise_for_status()
    except Exception as e:
        raise exceptions.HTTPException(501, "Could not connect to upstream API") from e

    try:  # convert response from API
        best_result = response.json()[0]
        lat = best_result["lat"]
        long = best_result["lon"]
        result = {"lat": lat, "long": long}
    except Exception as e:
        raise exceptions.HTTPException(
            501, "Upstream API returned unexpected response"
        ) from e

    return result


@app.get("/weather")
def weather(lat: float, long: float):
    print(f"Getting weather for {lat}, {long}")
    url = "https://api.open-meteo.com"

    # &current=temperature_2m
    payload = {"latitude": lat, "longitude": long, "current": "temperature_2m"}
    response = requests.get(f"{url}/v1/forecast", params=payload, timeout=2)  # type: ignore[arg-type]

    response.raise_for_status()

    print(response.status_code, response.content)
    return response.json()
