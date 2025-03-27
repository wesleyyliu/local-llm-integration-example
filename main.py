#!/usr/bin/env python3

import helper

import json
import sys

import loguru
import openai
import requests


# Set some constants for the model and server
BASE_MODEL = "phi-3.1-mini-128k-instruct"
BASE_HOST = "http://127.0.0.1:1234/v1"
BASE_COMPLETIONS_URL = f"{BASE_HOST}/completions"


# Configure loguru: initially set to INFO (students can change to DEBUG as needed)
loguru.logger.remove()
loguru.logger.add(sys.stderr, level="INFO")


# 1) Direct JSON POST approach
def call_model_directly(
    prompt: str,
    model: str = BASE_MODEL,
    url: str = BASE_COMPLETIONS_URL,
) -> dict:
    """
    Sends a prompt to the local LM Studio server's /v1/completions endpoint
    using a raw JSON POST (via the 'requests' library). Returns the
    raw JSON response as a Python dictionary.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 200,  # increase tokens for data extraction tasks
        "temperature": 0.0,  # set lower temperature for more deterministic output
    }

    loguru.logger.debug("Sending POST request to {} with payload: {}", url, payload)

    response = requests.post(url, json=payload)
    response.raise_for_status()

    # Extract the response to the prompt from the response to this query
    json_object = response.json()

    loguru.logger.debug("Received response: {}", json.dumps(json_object))

    # Check if the response contains 'choices' and 'text'
    if "choices" in json_object and len(json_object["choices"]) > 0:

        # Extract the text from the first choice
        text_object = json_object["choices"][0]["text"]

        loguru.logger.debug("Extracted text: {}", text_object)

        return text_object
    else:
        raise ValueError("Unexpected response format: 'choices' not found")


# 2) OpenAI SDK v1 approach
def call_model_openai_sdk(
    prompt: str, model: str = BASE_MODEL, host: str = BASE_HOST
) -> str:
    """
    Sends a prompt to the local LM Studio server using the OpenAI v1 SDK.
    Returns the text of the model's first completion.

    Note: we provide a 'DUMMY_KEY' for api_key, since LM Studio doesn't require
    real credentials for local usage. We also override the base_url to point
    at the local LM Studio server.
    """
    client = openai.OpenAI(
        api_key="DUMMY_KEY",  # LM Studio doesn't need a real key
        base_url=host,  # LM Studio server URL
    )

    loguru.logger.debug(
        "Using OpenAI SDK with model: {}, host: {}, prompt: {}", model, host, prompt
    )

    # The local model is used via the standard "completions" interface
    response = client.completions.create(
        model=model, prompt=prompt, max_tokens=200, temperature=0.0
    )

    loguru.logger.debug("Received response from OpenAI SDK: {}", response)

    # Extract the text from the first choice
    text_object = response.choices[0].text

    loguru.logger.debug("Extracted text from OpenAI SDK: {}", text_object)

    # Return only the text from the first completion
    return text_object


def main():
    # Example: Extracting Email Addresses
    data_extraction_prompt = """Extract all email addresses from the text below. Provide the emails in a JSON list.

Text:
"Hello David, please reach out to sarah.jones@example.com and support@mycompany.org.
Also, don’t forget to CC marketing-team@website.co.uk."
"""

    # 1) Call via direct JSON POST
    direct_response = call_model_directly(data_extraction_prompt)
    loguru.logger.debug("[Direct JSON POST] Output from the call:")
    loguru.logger.debug(direct_response)

    direct_response_json = helper.extract_json(direct_response)
    loguru.logger.info("[Direct JSON POST] Extracted JSON:")
    loguru.logger.info(direct_response_json)

    # 2) Call via OpenAI SDK
    sdk_response = call_model_openai_sdk(data_extraction_prompt)
    loguru.logger.debug("[OpenAI SDK] Output from the call:")
    loguru.logger.debug(sdk_response)
    sdk_response_json = helper.extract_json(sdk_response)
    loguru.logger.info("[OpenAI SDK] Extracted JSON:")
    loguru.logger.info(sdk_response_json)


if __name__ == "__main__":
    helper.check_lm_studio_server(base_url=BASE_HOST, requested_model=BASE_MODEL)
    main()
