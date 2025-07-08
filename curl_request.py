import json

import requests
from typing import Optional, Dict, Any, Union, Tuple

def response_to_json(response):
    response_data = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "url": response.url,
        "reason": response.reason,
        "elapsed": response.elapsed.total_seconds(),
        "encoding": response.encoding,
        "text": response.text,  # or response.content.decode('utf-8')
        # Optionally parse JSON response body:
        "json": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else None,
    }

    return json.dumps(response_data, indent=2)

def send_curl_request(
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        json: Optional[str] = None,
        data: Optional[str] = None,
) -> requests.Response:
    """
    General-purpose HTTP request function mimicking curl-style requests.

    :param method: HTTP method (e.g., "GET", "POST", etc.)
    :param url: Full URL to request
    :param headers: Dictionary of headers
    :param params: URL query parameters
    :param json: JSON body
    :param data: Raw or form data
    :return: `requests.Response` object
    """
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        params=params,
        json=json,
        data=data,
    )
    return response_to_json(response)