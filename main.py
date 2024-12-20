import ollama
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
import logging
import json
import weather_function
import types

config_file_name = "config.json"

try:
    with open(config_file_name) as config_file:
        data = json.load(config_file)
        context = data['context']
        model_name = data['model_name']
        weather_function.geocoding_url = data['geocoding_url']
        weather_function.weather_api_url = data['weather_api_url']
        tools = data['tools']
except Exception as e:
    logging.error(f"Error occurred while fetching config: {str(e)}")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
model = OllamaFunctions(model=model_name, format="json", temperature=0)
model = model.bind_tools(tools=tools)
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=context),
    ("human", "{input}"),
])


def process_query(query):
    logging.info(f"Processing query: {query}")
    formatted_prompt = prompt.format_messages(input=query)
    result = model.invoke(formatted_prompt)
    logging.info(f"Model result: {result}")

    if result.tool_calls:
        for tool_call in result.tool_calls:
            function_name = tool_call['name']
            args = tool_call['args']
            logging.info(f"Function call: {function_name}, Args: {args}")

            if function_name == "get_current_weather":
                weather_request_output = weather_function.process_weather_request(**args)
                messages = [
                    {"role": "assistant", "content": context},
                    {"role": "user", "content": query},
                    {"role": "tool", "name": function_name, "content": weather_request_output},
                    {"role": "user", "content": f"Say information from tool about current weather in provided "
                                                f"location. Api response: {weather_request_output}"}
                ]

                stream = ollama.chat(
                    model=model_name,
                    messages=messages,
                    stream=True
                )

                return stream
    return result.content


def print_model_response(response):
    if isinstance(response, types.GeneratorType):
        for chunk in response:
            print(chunk['message']['content'], end='')
    else:
        print(response)


if __name__ == "__main__":
    while True:
        print()
        message = input(">>> ")
        if message == "/exit":
            break
        output = process_query(message)
        print_model_response(output)



