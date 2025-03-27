import json
import re

import loguru
import requests


def check_lm_studio_server(
    base_url: str = "http://127.0.0.1:1234/v1",
    requested_model: str = "phi-3.1-mini-128k-instruct",
) -> None:
    """
    Verifies that the LM Studio server is running at `base_url`,
    that we can query `/models`, we receive a valid response,
    and that `requested_model` is among the available models.

    Raises:
        ConnectionError: if the server or endpoint is not reachable
        ValueError: if no models are returned, or the requested model is not found
    """
    # 1) Check if the host is live
    try:
        # Attempt a basic GET on the base_url (or any known endpoint) to verify it's listening
        r = requests.get(base_url, timeout=3)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(
            f"Cannot connect to LM Studio server at {base_url}. Error: {e}"
        )

    # 2) Query the /models endpoint
    models_endpoint = f"{base_url}/models"
    try:
        response = requests.get(models_endpoint, timeout=3)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(
            f"Failed to query /models at {models_endpoint}. Error: {e}"
        )

    # 3) Check that we got valid JSON, and that it has the structure we expect
    data = response.json()
    print(data)
    if "data" not in data or not isinstance(data["data"], list):
        raise ValueError("The /models response did not contain 'data' as a list.")

    # 4) Check that the requested model is in the list
    model_ids = [m.get("id") for m in data["data"] if "id" in m]
    if requested_model not in model_ids:
        raise ValueError(
            f"Requested model '{requested_model}' is not available. "
            f"Available models: {model_ids}"
        )

    print(
        f"Success! {requested_model} is available on the LM Studio server at {base_url}."
    )


def extract_json(text: str):
    """
    Extracts a JSON snippet from a text string.
    This function looks for content enclosed within ```json ... ``` fences.
    If not found, it tries to parse the entire text.
    Returns a Python object (e.g. list or dict) or None if parsing fails.
    """
    pattern = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)
    match = pattern.search(text)
    if match:
        json_str = match.group(1)
    else:
        # Fallback: assume the whole text is JSON
        json_str = text

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
