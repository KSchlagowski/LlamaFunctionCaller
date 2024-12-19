# 17.12.2024 22:04 Ollama.py backup

import ollama
# import chainlit as cl
import requests
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model_name = "llama3.2:3b"
weather_api_url = "https://api.open-meteo.com/v1/forecast"
geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

tools = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA. It can be only city name as well, e.g. Berlin.",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location"],
        },
    },
]

model = OllamaFunctions(model=model_name, format="json", temperature=0)
model = model.bind_tools(tools=tools)

messages = []

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="You are a helpful AI assistant that has a purpose to check weather conditions in cities around the world. If user asks you about weather always use given tools."),
    ("human", "{input}"),
])


def generate_response(message):
    messages.append(
        {'role': 'user', 'content': message}
    )

    stream = ollama.chat(
        model=model_name,
        messages=messages,
        stream=True
    )

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
        response = response + part

    messages.append(
        {
            'role': 'assistant',
            'content': response,
        }
    )


def get_current_weather(location, unit="celsius"):
    logging.info(f"Getting weather for {location}")

    params = {
        "latitude": 0,
        "longitude": 0,
        "current_weather": "true",
        "temperature_unit": unit
    }

    location_parts = location.split(',')
    city = location_parts[0].strip()
    country = location_parts[1].strip() if len(location_parts) > 1 else ""

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        logging.info(f"Fetching coordinates for {location}")
        geo_response = requests.get(geocoding_url, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        logging.debug(f"Geocoding response: {geo_data}")

        # If first attempt fails, try with full location string
        if "results" not in geo_data or not geo_data["results"]:
            geo_params["name"] = location
            geo_response = requests.get(geocoding_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            logging.debug(f"Second geocoding attempt response: {geo_data}")

        # Extract coordinates if found
        if "results" in geo_data and geo_data["results"]:
            params["latitude"] = geo_data["results"][0]["latitude"]
            params["longitude"] = geo_data["results"][0]["longitude"]
            logging.info(
                f"Coordinates found: {params['latitude']}, {params['longitude']}")
        else:
            logging.warning(f"No results found for location: {location}")
            return f"Sorry, I couldn't find the location: {location}"

        # Fetch weather data using coordinates
        logging.info("Fetching weather data")
        response = requests.get(weather_api_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        logging.debug(f"Weather data response: {weather_data}")

        # Extract and format weather information
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
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching weather data: {str(e)}")
        return f"An error occurred while fetching weather data: {str(e)}"


def process_query(query):
    logging.info(f"Processing query: {query}")
    formatted_prompt = prompt.format_messages(input=query)
    logging.info(f"Formatted prompt: {formatted_prompt}")
    result = model.invoke(formatted_prompt)
    logging.info(f"Model result: {result}")

    if result.tool_calls:
        for tool_call in result.tool_calls:
            function_name = tool_call['name']
            args = tool_call['args']
            logging.info(f"Function call: {function_name}, Args: {args}")

            if function_name == "get_current_weather":
                return get_current_weather(**args)
    print(result.content)
    return result.content
    #generate_response(result.content)

while 1:
    print("")
    message = input(">>> ")
    if message == "/exit":
        break
    process_query(message)
    #generateResponse(prompt)
    print()
