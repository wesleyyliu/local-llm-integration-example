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
        ConnectionError: if the server or endpoint is not reachable.
        ValueError: if no models are returned, or the requested model is not found.
    """
    loguru.logger.debug("Checking LM Studio server at base URL: {}", base_url)

    # 1) Check if the host is live
    try:
        r = requests.get(base_url, timeout=3)
        r.raise_for_status()
        loguru.logger.debug("Server at {} is live", base_url)
    except requests.exceptions.RequestException as e:
        loguru.logger.error("Cannot connect to LM Studio server at {}: {}", base_url, e)
        raise ConnectionError(
            f"Cannot connect to LM Studio server at {base_url}. Error: {e}"
        )

    # 2) Query the /models endpoint
    models_endpoint = f"{base_url}/models"
    loguru.logger.debug("Querying models endpoint: {}", models_endpoint)
    try:
        response = requests.get(models_endpoint, timeout=3)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        loguru.logger.error("Failed to query /models at {}: {}", models_endpoint, e)
        raise ConnectionError(
            f"Failed to query /models at {models_endpoint}. Error: {e}"
        )

    # 3) Check that we got valid JSON, and that it has the structure we expect
    data = response.json()
    loguru.logger.debug("Received data from models endpoint: {}", json.dumps(data))
    if "data" not in data or not isinstance(data["data"], list):
        loguru.logger.error("The /models response did not contain 'data' as a list.")
        raise ValueError("The /models response did not contain 'data' as a list.")

    # 4) Check that the requested model is in the list
    model_ids = [m.get("id") for m in data["data"] if "id" in m]
    if requested_model not in model_ids:
        loguru.logger.error(
            "Requested model '{}' not found. Available models: {}",
            requested_model,
            model_ids,
        )
        raise ValueError(
            f"Requested model '{requested_model}' is not available. Available models: {model_ids}"
        )

    loguru.logger.info(
        "Success! {} is available on the LM Studio server at {}.",
        requested_model,
        base_url,
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
        loguru.logger.debug("Found JSON snippet in text: {}", json_str)
    else:
        json_str = text
        loguru.logger.debug(
            "No JSON snippet found; using full text for JSON parsing: {}", json_str
        )

    try:
        parsed = json.loads(json_str)
        loguru.logger.debug("Successfully parsed JSON: {}", parsed)
        return parsed
    except json.JSONDecodeError as e:
        loguru.logger.error("Error decoding JSON: {}", e)
        return None
