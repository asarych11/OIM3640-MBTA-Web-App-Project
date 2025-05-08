"""
The file connects to two APIs Mapbox API (turns place into a latitude and longtitude) and MBTA API (finds the nearest MBTA station near that lat/lon) 
and then prints the nearest MBTA stop name and whether it's wheelchair accessible.
"""

import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it
 
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))
    

def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    encoded_location = urllib.parse.quote(place_name) # format the place name for a URL
    url = f"{MAPBOX_BASE_URL}/{encoded_location}.json?access_token={MAPBOX_TOKEN}&limit=1" # build the full URL to ask Mapbox for lat/lng
    data = get_json(url) # convert get_json response into a dictionary
    coords = data["features"][0]["geometry"]["coordinates"] # grab the coordinates from the response (Mapbox returns [longtitude,latitude])
    return str(coords[1]), str(coords[0]) # return the coordinates (latitude, longtitude) as strings


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = ( # vuild the request url for MBTA API
        f"{MBTA_BASE_URL}?"
        f"api_key={MBTA_API_KEY}&"
        f"filter[latitude]={latitude}&"
        f"filter[longitude]={longitude}&"
        f"sort=distance"
    )
    data = get_json(url) # get the API response as dictionary
    
    if not data["data"]:  # added this after the code returned index error with locations like Fenway Park and Prudential Center
        print("No nearby MBTA stops found.")
        return "No stop found", False, "N/A"

    stop = data["data"][0] # extract the nearest stop
    name = stop['attributes']['name']
    stop_id = stop['id']

    wheelchair_code = stop['attributes']['wheelchair_boarding'] # get accessibility info (1 = yes, 2 = no, 0 = unknown)
    accessible = wheelchair_code == 1

    return name, accessible, stop_id

# def get_predictions_for_stop(stop_id: str) -> list:
    # url = 

def find_stop_near(place_name: str) -> tuple[str, bool, str]:
    """
    Given a place name or address, returns the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    lat, lng = get_lat_lng(place_name) # assign coordinates to new variables
    return get_nearest_station(lat,lng) # return the nearby MBTA station using the previous function

from datetime import datetime

def get_predictions_for_stop(stop_id: str) -> str | None:
    """
    Given a stop ID, return the soonest departure time (as a formatted string) for that stop.
    Returns None if no valid departure time is found.
    """
    url = f"https://api-v3.mbta.com/predictions?filter[stop]={stop_id}&sort=departure_time&api_key={MBTA_API_KEY}"
    data = get_json(url)
    predictions = data.get("data", [])

    for prediction in predictions:
        departure_time = prediction["attributes"].get("departure_time")
        if departure_time:
            # format for easy display
            dt = datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
            return dt.strftime("%H:%M")

    return None  # if no departure time found

def main():
    """
    You should test all the above functions here
    """
    place = input(f"Please enter the name of the place: ")

    stop_name, is_accessible, stop_id = find_stop_near(place)

    departure_time = get_predictions_for_stop(stop_id)

    if departure_time:
        print(f"The nearest MBTA stop to '{place}': '{stop_name}'. The earliest departure time from this stop is '{departure_time}'.")
    else:
        print(f"The nearest MBTA stop to '{place}': '{stop_name}', but no upcoming departures were found.")

    if is_accessible == True:
        print("Wheelchair accessible.")
    else:
        print("Not wheelchair accessible.")


if __name__ == "__main__":
    main()