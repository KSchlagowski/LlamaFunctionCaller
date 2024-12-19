import ollama
# import chainlit as cl
import requests
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
import logging
import json

geocoding_url = ''
weather_api_url = ''


def get_location_coordinates(location, params_for_geo_api, unit):
    geo_params_for_weather_api = {
        "latitude": 0,
        "longitude": 0,
        "current_weather": "true",
        "temperature_unit": unit
    }

    logging.info(f"Fetching coordinates for {location}")
    geo_response = requests.get(geocoding_url, params=params_for_geo_api)
    geo_response.raise_for_status()
    geo_data = geo_response.json()
    logging.debug(f"Geocoding response: {geo_data}")

    # If first attempt fails, try with full location string
    if "results" not in geo_data or not geo_data["results"]:
        params_for_geo_api["name"] = location
        geo_response = requests.get(geocoding_url, params=params_for_geo_api)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        logging.debug(f"Second geocoding attempt response: {geo_data}")

    # Extract coordinates if found
    if "results" in geo_data and geo_data["results"]:
        geo_params_for_weather_api["latitude"] = geo_data["results"][0]["latitude"]
        geo_params_for_weather_api["longitude"] = geo_data["results"][0]["longitude"]
        logging.info(
            f"Coordinates found: {geo_params_for_weather_api['latitude']}, {geo_params_for_weather_api['longitude']}")
        return geo_params_for_weather_api
    else:
        logging.warning(f"No results found for location: {location}")
        return f"Sorry, I couldn't find the location: {location}"


def get_current_weather(location, geo_params_for_weather_api, unit):
    logging.info("Fetching weather data")
    response = requests.get(weather_api_url, params=geo_params_for_weather_api)
    response.raise_for_status()
    weather_data = response.json()
    logging.debug(f"Weather data response: {weather_data}")

    if "current_weather" in weather_data:
        current_weather = weather_data["current_weather"]
        temp = current_weather["temperature"]
        wind_speed = current_weather["windspeed"]

        result = f"The current weather in {location} is {temp}°{unit.upper()} with a wind speed of {wind_speed} km/h."
        logging.info(f"Weather result: {result}")
        return result
    else:
        logging.warning(f"No current weather data found for {location}")
        return f"Sorry, I couldn't retrieve weather data for {location}"


def process_weather_request(location, unit="celsius"):
    logging.info(f"Getting weather for {location}")

    location_parts = location.split(',')
    city = location_parts[0].strip()

    params_for_geo_api = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        geo_params_for_weather_api = get_location_coordinates(location, params_for_geo_api, unit)
        weather_info = get_current_weather(location, geo_params_for_weather_api, unit)
        return weather_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching weather data: {str(e)}")
        return f"An error occurred while fetching weather data: {str(e)}"