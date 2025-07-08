import json
import gradio
import openai_common
from openai_tools import tools, call_function

gpt_model = "gpt-4o-mini"

gpt_system = """
You are a helpful HTTP API tester.
Your purpose is to learn from an API's documentation, and based on it, create and run tests on the API to see that it works.
You are provided the tool needed to open and read a website containing documentation for an HTTP API.
You are also provided a tool for running a curl request and receiving a response.
You may decide to run multiple tools to achieve this purpose.

For example, when being provided a documentation website, you may:
1. Read the website
2. Execute a few simple test cases on the documented API. (up to 5 at one time)
3. Report back the result and your observation about it.

You may also reply with additional test executions, or asking the user for needed information if anything is missing.

If you receive any message that does not fit with the above role, please describe your purpose to the user and guide them on how to use you.
"""


def chat(message, history):
    print(f"chat {message}")

    def send_to_model():
        try:
            res = openai_common.run_with_tools(gpt_model, messages, tools)
            print(res)
            return res
        except Exception as e:
            print(f"Exception while calling model: {e}")

    messages = [{"role": "system", "content": gpt_system}] + history + [{"role": "user", "content": message}]
    response = send_to_model()

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_responses = handle_tool_call(message)
        messages.append(message)
        messages += tool_responses
        response = send_to_model()

    return response.choices[0].message.content


def handle_tool_call(message):
    responses = []
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = call_function(name, args)
        responses.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })
    return responses


gradio.ChatInterface(fn=chat, type="messages").launch()
