# Local LLM Integration Example

This repository demonstrates how to integrate a **Local Language Model** into a Python application. While public LLM APIs (e.g., OpenAI, Cohere) are popular, they can be **expensive** or **rate-limited**. These limits are enough to reduce how much exploration a programmer does.

By experimenting with a **locally hosted** model, you can freely explore prompt engineering, data extraction, and more—without incurring API costs.

We're using a **2GB-sized** model (`phi-3.1-mini-128k-instruct`) for simplicity, but you can also experiment with larger models (e.g., 20GB, like Cohere's Command R) for more advanced tasks. This local setup is enough to try out basic tasks such as structured data extraction from text.

## Why a Local LLM?

- **Cost-Effective**: No pay-per-call API fees.  
- **Faster Iteration**: Experiments run locally, no network latency.  
- **Privacy**: Your data never leaves your machine.

## Sample Prompt

In this application, we will use the following sample prompt to extract email addresses from text:

You can find several other potential prompts in the `SAMPLE-PROMPTS.md` file.

### Extracting Email Addresses

**Prompt:**
```
Extract all email addresses from the text below. Provide the emails in a JSON list.

Text:
"Hello David, please reach out to sarah.jones@example.com and support@mycompany.org. 
Also, don’t forget to CC marketing-team@website.co.uk."
```
**Expected Output (Example):**
```
[
  "sarah.jones@example.com",
  "support@mycompany.org",
  "marketing-team@website.co.uk"
]
```

## Installation & Setup

### 1. Install LM Studio

1. **Download LM Studio** from [lmstudio.ai](https://lmstudio.ai/).  
2. Follow the installation instructions for your operating system.  
3. Start LM Studio, and verify it's running on `http://127.0.0.1:1234` (the default).  

> **Tip**: If LM Studio doesn't start on that port, check its Preferences > API settings.

### 2. Model Configuration

1. **Search for a Model**: In LM Studio, click **Models** → **Add New Model** (or something similar) to browse available models.  
2. **Install the `phi-3.1-mini-128k-instruct` Model**: This is a ~2GB model that can handle simple tasks like data extraction. It's enough to demonstrate the flow without using too much GPU/CPU.  
3. **Load Your Model**: In LM Studio, ensure the newly downloaded model is loaded and “running” (LM Studio usually shows a green check or “ready” status).  
4. **Check the API**: Confirm that LM Studio's local server is running by visiting [http://127.0.0.1:1234/v1/models](http://127.0.0.1:1234/v1/models). You should see a JSON list of models, including `"phi-3.1-mini-128k-instruct"`.

### 3. Local Environment Setup

This repo uses **pipenv** for dependency management. Make sure you have Python 3.12 (or similar) installed.

1. **Fork (or import/copy)** this repository to your own GitHub account, keep the name `local-llm-integration-example`.

2. **Clone** this repository (e.g., via GitHub).  

3. **Install Dependencies**:
   ```bash
   pipenv install
   ```
   This will install `requests`, `openai`, and `loguru`.

4. **Run the Script**:
   ```bash
   pipenv run python main.py
   ```
   - The script will:
     1. Check that LM Studio is up and that your requested model is available.
     2. Send a prompt to the model to extract data (e.g., email addresses).
     3. Print out the raw or parsed JSON response.

### Suggestions for Experimentation

1. **Change Log Level to DEBUG**  
   In `main.py`, the line:
   ```python
   loguru.logger.add(sys.stderr, level="INFO")
   ```
   sets the default log level. Change `"INFO"` to `"DEBUG"` if you'd like to see more detailed logs about request payloads and model responses.

2. **Inspect the JSON Outputs**  
   Each request's text output is **attempted** to be parsed as JSON via `helper.extract_json()`. Sometimes the model includes extra text or formatting around the JSON. If you want to pretty-print the final JSON, you can use tools like [jsonformatter.org/json-pretty-print](https://jsonformatter.org/json-pretty-print) or Python's `json.dumps(obj, indent=2)` in your code.

3. **Try Different Prompts**  
   The included example asks for email extraction. You can experiment with other data-extraction tasks (like phone numbers, product details, or structured outputs). Adjust the prompt in `main.py` and see how the local model handles it.

---

Happy experimenting with your **Local LLM**! If you run into issues, make sure that:
1. LM Studio is running and the correct port (default: `1234`) is used.  
2. Your model is actually loaded in LM Studio and shows up in `GET /v1/models`.  
3. You have enough system resources to run the model (2GB in memory usage or more, depending on your hardware).

Enjoy building your own offline GPT-like applications!