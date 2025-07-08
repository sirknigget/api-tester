from curl_request import send_curl_request
from website import Website


def open_website(url):
    website = Website(url)
    return website.text


website_function = {
    "name": "open_website",
    "description": "Open a website and read its content",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The website URL to open",
            },
        },
        "required": ["url"],
        "additionalProperties": False
    }
}

curl_function = {
    "name": "send_curl_request",
    "description": "Send a curl-style HTTP request to any URL with full customization.",
    "parameters": {
        "type": "object",
        "properties": {
            "method": {
                "type": "string",
                "description": "HTTP method to use, e.g., GET, POST, PUT, DELETE."
            },
            "url": {
                "type": "string",
                "description": "The full URL to send the request to."
            },
            "headers": {
                "type": "object",
                "description": "Optional HTTP headers to include in the request.",
                "additionalProperties": {"type": "string"}
            },
            "params": {
                "type": "object",
                "description": "Optional URL query parameters.",
                "additionalProperties": {"type": "string"}
            },
            "json": {
                "description": "JSON body payload for the request.",
                "type": "string"
            },
            "data": {
                "description": "Raw string, form data, or binary payload.",
                "type": "string"
            },
        },
        "required": ["method", "url"]
    }
}

tools = [{"type": "function", "function": website_function},
         {"type": "function", "function": curl_function}]

function_names = {"open_website": open_website, "send_curl_request": send_curl_request}


def call_function(name, args):
    print(f"call function {name} with args {args}")
    function = function_names[name]
    result = function(**args)
    print(f"function result: {result}")
    return result
