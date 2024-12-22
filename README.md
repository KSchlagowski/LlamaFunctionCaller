# LlamaFunctionCaller

## Project Overview

This project is an Python-based AI-powered chatbot that can fetch real-time weather data. It leverages the LangChain and Ollama models to interpret user input and fetch weather data. This assistant demonstrates the integration of AI with external APIs and prompt engineering to perform practical tasks like weather forecasting.

## Features

- **Real-time Weather Updates**: Retrieves weather data for any specified location.
- **Scalable Design**: Modular design make it easily extendable to support more API integrations or functions.
- **AI-driven**: Uses LangChain and Ollama for natural language understanding and response generation.

## How It Works
The project uses a language model from Ollama, enhanced by LangChain's function calling capability, to process queries. When a user inputs a query, the model determines if a weather request is necessary. If so, it calls a function to fetch weather data using geolocation and weather APIs.

![Gif](https://github.com/user-attachments/assets/aab4ccb1-5ca0-4f11-a66e-be4ab54f0e8e)

## File Structure
- **main.py** – The core of the application that handles user input and model interaction.
- **weather_function.py** – Contains functions to handle geocoding and weather data retrieval from APIs.
- **config.json** – Configuration file specifying API URLs and model parameters.
- **requirements.txt** – Lists all necessary Python packages for the project.

## Requirements

- Python 3.7 or later
- Ollama installed and running
- Internet connection (for API requests)

## Dependencies

Install the necessary packages by running:

```
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
ollama
langchain
langchain_experimental
requests
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ollama-ai-chatbot.git](https://github.com/KSchlagowski/LlamaFunctionCaller.git
   cd LlamaFunctionCaller
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Ensure Ollama is installed and running. Refer to [Ollama documentation](https://github.com/jmorganca/ollama) for installation instructions.

## Usage

1. Run the chatbot:
   ```
   python main.py
   ```
2. Interact with the chatbot by entering queries like:
   - "What's the weather in London?"
   - "Weather in Tokyo"
3. Type `/exit` to stop the chatbot.

### How it Works

1. **User Input**: User enters a query (e.g., "Weather in Paris").
2. **AI Processing**: Ollama processes the input and identifies the intent (weather request).
3. **Function Call**: The chatbot calls the relevant function (weather retrieval).
4. **API Call**: The bot fetches data from Open-Meteo API.
5. **Response**: The chatbot displays the result in the console.

## APIs Used

- **Geocoding**: [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- **Weather**: [Open-Meteo Weather API](https://open-meteo.com/)

## Configuration
Modify `config.json` to update API URLs or model parameters. The default configuration uses Open Meteo's APIs.

## Troubleshooting

- **API Errors**: Ensure the internet connection is active.
- **Configuration Issues**: Check `config.json` for API URLs.
- **Ollama Not Running**: Verify that Ollama is correctly installed and running.

## Future Improvements

- Add more external API integrations (e.g., news, currency conversion).
- Implement chatbot memory for longer conversations.
- Improve error handling and user interaction.

## License

This project is licensed under the MIT License.

## Author

[Kamil Schlagowski](https://github.com/KSchlagowski)






