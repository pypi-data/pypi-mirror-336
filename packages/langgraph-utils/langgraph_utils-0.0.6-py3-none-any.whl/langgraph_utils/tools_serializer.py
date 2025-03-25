from langchain_core.tools import StructuredTool
import json
import os
import requests

"""
Converts a list of langchain tool objects into a JSON string.

:param tools: List of tool objects to be serialized.
:return: JSON string representation of the tools.
"""
def create_tools_json(tools):
    tools_json = []
    for tool in tools:
        tool_info = {
            'name': tool.name,
            'description': tool.description,
            'args_schema': tool.args_schema.model_json_schema()
        }
        tools_json.append(tool_info)
    return tools_json



"""
Converts JSON formatted langchain tool into structured tool objects.
@param json_tools: A list or single JSON object representing tools.
@return: A list of StructuredTool objects or a single StructuredTool if only one is provided.
"""
def json_to_structured_tools(json_tools):
    if not isinstance(json_tools, list):
        json_tools = [json_tools]
    
    structured_tools = []
    for tool_json in json_tools:
            
        structured_tool = StructuredTool(
            name=tool_json['name'],
            description=tool_json['description'],
            func=None,
            args_schema=tool_json['args_schema']
        )
        structured_tools.append(structured_tool)
    
    return structured_tools if len(structured_tools) > 1 else structured_tools[0]



def call_model(llm, provider, messages, tools=None, params={}):
    """
    Calls an external LLM API via AWS API Gateway.

    Parameters:
    - llm (str): The model name to call.
    - provider (str): The LLM provider (e.g., OpenAI, Anthropic).
    - messages (list): Conversation history in message format.
    - tools (list, optional): List of tool definitions for the LLM to use.
    - params (dict, optional): Additional parameters for the LLM call (e.g., temperature, max tokens).

    Returns:
    - dict: The JSON response from the API.
    """
    # Prepare the payload for the API request
    data = {
        "provider": provider,
        "model_name": llm,
        "params": params,
        "messages": messages,
        "tools": tools
    }

    # Fetch API Gateway credentials from environment variables
    api_key = os.environ.get('API_GW_KEY')
    api_url = os.environ.get('API_GW_URL')

    if not api_key or not api_url:
        raise ValueError("Missing API Gateway key or URL. Ensure API_GW_KEY and API_GW_URL are set.")

    # Set the request headers
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    try:
        # Send a POST request to the API Gateway
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Error while calling LLM API: {e}")
