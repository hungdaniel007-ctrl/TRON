- [Supported Models & Providers](https://docs.litellm.ai/docs/providers)
- Deepseek

# Deepseek

[https://deepseek.com/](https://deepseek.com/)

**We support ALL Deepseek models, just set `deepseek/` as a prefix when sending completion requests**

## API Key

```
# env variableos.environ['DEEPSEEK_API_KEY']
```

## Sample Usage

```
from litellm import completionimport osos.environ['DEEPSEEK_API_KEY'] = ""response = completion(    model="deepseek/deepseek-chat",     messages=[       {"role": "user", "content": "hello from litellm"}   ],)print(response)
```

## Sample Usage - Streaming

```
from litellm import completionimport osos.environ['DEEPSEEK_API_KEY'] = ""response = completion(    model="deepseek/deepseek-chat",     messages=[       {"role": "user", "content": "hello from litellm"}   ],    stream=True)for chunk in response:    print(chunk)
```

## Supported Models - ALL Deepseek Models Supported!

We support ALL Deepseek models, just set `deepseek/` as a prefix when sending completion requests

| Model Name     | Function Call                                           |
| -------------- | ------------------------------------------------------- |
| deepseek-chat  | `completion(model="deepseek/deepseek-chat", messages)`  |
| deepseek-coder | `completion(model="deepseek/deepseek-coder", messages)` |

## Reasoning Models

| Model Name        | Function Call                                              |
| ----------------- | ---------------------------------------------------------- |
| deepseek-reasoner | `completion(model="deepseek/deepseek-reasoner", messages)` |

### Thinking / Reasoning Mode

Enable thinking mode for DeepSeek reasoner models using `thinking` or `reasoning_effort` parameters:

- thinking param
- reasoning_effort param

```
from litellm import completionimport osos.environ['DEEPSEEK_API_KEY'] = ""resp = completion(    model="deepseek/deepseek-reasoner",    messages=[{"role": "user", "content": "What is 2+2?"}],    thinking={"type": "enabled"},)print(resp.choices[0].message.reasoning_content)  # Model's reasoningprint(resp.choices[0].message.content)  # Final answer
```

note

DeepSeek only supports `{"type": "enabled"}` - unlike Anthropic, it doesn't support `budget_tokens`. Any `reasoning_effort` value other than `"none"` enables thinking mode.

### Basic Usage

- SDK
- PROXY

```
from litellm import completionimport osos.environ['DEEPSEEK_API_KEY'] = ""resp = completion(    model="deepseek/deepseek-reasoner",    messages=[{"role": "user", "content": "Tell me a joke."}],)print(    resp.choices[0].message.reasoning_content)
```


# Ollama

LiteLLM supports all models from [Ollama](https://github.com/ollama/ollama)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BerriAI/litellm/blob/main/cookbook/liteLLM_Ollama.ipynb)

info

We recommend using [ollama_chat](https://docs.litellm.ai/docs/providers/ollama#using-ollama-apichat) for better responses.

## Pre-requisites

Ensure you have your ollama server running

## Example usage

```
from litellm import completionresponse = completion(    model="ollama/llama2",     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],     api_base="http://localhost:11434")print(response)
```

## Example usage - Streaming

```
from litellm import completionresponse = completion(    model="ollama/llama2",     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],     api_base="http://localhost:11434",    stream=True)print(response)for chunk in response:    print(chunk['choices'][0]['delta'])
```

## Example usage - Streaming + Acompletion

Ensure you have async_generator installed for using ollama acompletion with streaming

```
pip install async_generator
```

```
async def async_ollama():    response = await litellm.acompletion(        model="ollama/llama2",         messages=[{ "content": "what's the weather" ,"role": "user"}],         api_base="http://localhost:11434",         stream=True    )    async for chunk in response:        print(chunk)# call async_ollamaimport asyncioasyncio.run(async_ollama())
```

## Example Usage - JSON Mode

To use ollama JSON Mode pass `format="json"` to `litellm.completion()`

```
from litellm import completionresponse = completion(  model="ollama/llama2",  messages=[      {          "role": "user",          "content": "respond in json, what's the weather"      }  ],  max_tokens=10,  format = "json")
```

## Example Usage - Tool Calling

To use ollama tool calling, pass `tools=[{..}]` to `litellm.completion()`

- SDK
- PROXY

```
from litellm import completionimport litellm ## [OPTIONAL] REGISTER MODEL - not all ollama models support function calling, litellm defaults to json mode tool calls if native tool calling not supported.# litellm.register_model(model_cost={#                 "ollama_chat/llama3.1": { #                   "supports_function_calling": true#                 },#             })tools = [  {    "type": "function",    "function": {      "name": "get_current_weather",      "description": "Get the current weather in a given location",      "parameters": {        "type": "object",        "properties": {          "location": {            "type": "string",            "description": "The city and state, e.g. San Francisco, CA",          },          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},        },        "required": ["location"],      },    }  }]messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]response = completion(  model="ollama_chat/llama3.1",  messages=messages,  tools=tools)
```

## Using Ollama FIM on `/v1/completions`

LiteLLM supports calling Ollama's `/api/generate` endpoint on `/v1/completions` requests.

- SDK
- PROXY

```
import litellm litellm._turn_on_debug() # turn on debug to see the requestfrom litellm import completionresponse = completion(    model="ollama/llama3.1",    prompt="Hello, world!",    api_base="http://localhost:11434")print(response)
```

## Using ollama `api/chat`

In order to send ollama requests to `POST /api/chat` on your ollama server, set the model prefix to `ollama_chat`

```
from litellm import completionresponse = completion(    model="ollama_chat/llama2",     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}], )print(response)
```

## Ollama Models

Ollama supported models: [GitHub - ollama/ollama: Get up and running with Kimi-K2.5, GLM-4.7, DeepSeek, gpt-oss, Qwen, Gemma and other models.](https://github.com/ollama/ollama)

| Model Name                  | Function Call                                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Mistral                     | `completion(model='ollama/mistral', messages, api_base="http://localhost:11434", stream=True)`                      |
| Mistral-7B-Instruct-v0.1    | `completion(model='ollama/mistral-7B-Instruct-v0.1', messages, api_base="http://localhost:11434", stream=False)`    |
| Mistral-7B-Instruct-v0.2    | `completion(model='ollama/mistral-7B-Instruct-v0.2', messages, api_base="http://localhost:11434", stream=False)`    |
| Mixtral-8x7B-Instruct-v0.1  | `completion(model='ollama/mistral-8x7B-Instruct-v0.1', messages, api_base="http://localhost:11434", stream=False)`  |
| Mixtral-8x22B-Instruct-v0.1 | `completion(model='ollama/mixtral-8x22B-Instruct-v0.1', messages, api_base="http://localhost:11434", stream=False)` |
| Llama2 7B                   | `completion(model='ollama/llama2', messages, api_base="http://localhost:11434", stream=True)`                       |
| Llama2 13B                  | `completion(model='ollama/llama2:13b', messages, api_base="http://localhost:11434", stream=True)`                   |
| Llama2 70B                  | `completion(model='ollama/llama2:70b', messages, api_base="http://localhost:11434", stream=True)`                   |
| Llama2 Uncensored           | `completion(model='ollama/llama2-uncensored', messages, api_base="http://localhost:11434", stream=True)`            |
| Code Llama                  | `completion(model='ollama/codellama', messages, api_base="http://localhost:11434", stream=True)`                    |
| Llama2 Uncensored           | `completion(model='ollama/llama2-uncensored', messages, api_base="http://localhost:11434", stream=True)`            |
| Meta LLaMa3 8B              | `completion(model='ollama/llama3', messages, api_base="http://localhost:11434", stream=False)`                      |
| Meta LLaMa3 70B             | `completion(model='ollama/llama3:70b', messages, api_base="http://localhost:11434", stream=False)`                  |
| Orca Mini                   | `completion(model='ollama/orca-mini', messages, api_base="http://localhost:11434", stream=True)`                    |
| Vicuna                      | `completion(model='ollama/vicuna', messages, api_base="http://localhost:11434", stream=True)`                       |
| Nous-Hermes                 | `completion(model='ollama/nous-hermes', messages, api_base="http://localhost:11434", stream=True)`                  |
| Nous-Hermes 13B             | `completion(model='ollama/nous-hermes:13b', messages, api_base="http://localhost:11434", stream=True)`              |
| Wizard Vicuna Uncensored    | `completion(model='ollama/wizard-vicuna', messages, api_base="http://localhost:11434", stream=True)`                |

### JSON Schema support

- SDK
- PROXY

```
from litellm import completionresponse = completion(    model="ollama_chat/deepseek-r1",     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],     response_format={"type": "json_schema", "json_schema": {"schema": {"type": "object", "properties": {"name": {"type": "string"}}}}},)print(response)
```

## Ollama Vision Models

| Model Name | Function Call                          |
| ---------- | -------------------------------------- |
| llava      | `completion('ollama/llava', messages)` |

#### Using Ollama Vision Models

Call `ollama/llava` in the same input/output format as OpenAI [`gpt-4-vision`](https://docs.litellm.ai/docs/providers/openai#openai-vision-models)

LiteLLM Supports the following image types passed in `url`

- Base64 encoded svgs

**Example Request**

```
import litellmresponse = litellm.completion(  model = "ollama/llava",  messages=[      {          "role": "user",          "content": [                          {                              "type": "text",                              "text": "Whats in this image?"                          },                          {                              "type": "image_url",                              "image_url": {                              "url": "iVBORw0KGgoAAAANSUhEUgAAAG0AAABmCAYAAADBPx+VAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAA3VSURBVHgB7Z27r0zdG8fX743i1bi1ikMoFMQloXRpKFFIqI7LH4BEQ+NWIkjQuSWCRIEoULk0gsK1kCBI0IhrQVT7tz/7zZo888yz1r7MnDl7z5xvsjkzs2fP3uu71nNfa7lkAsm7d++Sffv2JbNmzUqcc8m0adOSzZs3Z+/XES4ZckAWJEGWPiCxj ... 1Mfl1ScP36ddcUaMuv24iOJtz7sbUjTS4qBvKmstYJoUauiuD3k5qhyr7QdUHMeCgLa1Ear9NquemdXgmum4fvJ6w1lqsuDhNrg1qSpleJK7K3TF0Q2jSd94uSZ60kK1e3qyVpQK6PVWXp2/FC3mp6jBhKKOiY2h3gtUV64TWM6wDETRPLDfSakXmH3w8g9Jlug8ZtTt4kVF0kLUYYmCCtD/DrQ5YhMGbA9L3ucdjh0y8kOHW5gU/VEEmJTcL4Pz/f7mgoAbYkAAAAAElFTkSuQmCC"                              }                          }                      ]      }  ],)print(response)
```

## LiteLLM/Ollama Docker Image

For Ollama LiteLLM Provides a Docker Image for an OpenAI API compatible server for local LLMs - llama2, mistral, codellama

[![Chat on WhatsApp](https://img.shields.io/static/v1?label=Chat%20on&message=WhatsApp&color=success&logo=WhatsApp&style=flat-square)](https://wa.link/huol9n) [![Chat on Discord](https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square)](https://discord.gg/wuPM9dRgDw)

### An OpenAI API compatible server for local LLMs - llama2, mistral, codellama

### Quick Start:

Docker Hub: For ARM Processors: https://hub.docker.com/repository/docker/litellm/ollama/general For Intel/AMD Processors: to be added

```
docker pull litellm/ollama
```

```
docker run --name ollama litellm/ollama
```

#### Test the server container

On the docker container run the `test.py` file using `python3 test.py`

### Making a request to this server

```
import openaiapi_base = f"http://0.0.0.0:4000" # base url for serveropenai.api_base = api_baseopenai.api_key = "temp-key"print(openai.api_base)print(f'LiteLLM: response from proxy with streaming')response = openai.chat.completions.create(    model="ollama/llama2",     messages = [        {            "role": "user",            "content": "this is a test request, acknowledge that you got it"        }    ],    stream=True)for chunk in response:    print(f'LiteLLM: streaming response from proxy {chunk}')
```

### Responses from this server

```
{  "object": "chat.completion",  "choices": [    {      "finish_reason": "stop",      "index": 0,      "message": {        "content": " Hello! I acknowledge receipt of your test request. Please let me know if there's anything else I can assist you with.",        "role": "assistant",        "logprobs": null      }    }  ],  "id": "chatcmpl-403d5a85-2631-4233-92cb-01e6dffc3c39",  "created": 1696992706.619709,  "model": "ollama/llama2",  "usage": {    "prompt_tokens": 18,    "completion_tokens": 25,    "total_tokens": 43  }}
```

## Calling Docker Container (host.docker.internal)

[Follow these instructions](https://github.com/BerriAI/litellm/issues/1517#issuecomment-1922022209/)

- [Supported Models & Providers](https://docs.litellm.ai/docs/providers)
- OpenRouter

# OpenRouter

LiteLLM supports all the text / chat / vision / embedding models from [OpenRouter](https://openrouter.ai/docs)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BerriAI/litellm/blob/main/cookbook/LiteLLM_OpenRouter.ipynb)

## Usage

```
import osfrom litellm import completionos.environ["OPENROUTER_API_KEY"] = ""os.environ["OPENROUTER_API_BASE"] = "" # [OPTIONAL] defaults to https://openrouter.ai/api/v1os.environ["OR_SITE_URL"] = "" # [OPTIONAL]os.environ["OR_APP_NAME"] = "" # [OPTIONAL]response = completion(            model="openrouter/google/palm-2-chat-bison",            messages=messages,        )
```

## Configuration with Environment Variables

For production environments, you can dynamically configure the base_url using environment variables:

```
import osfrom litellm import completion# Configure with environment variablesOPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")OPENROUTER_BASE_URL = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")# Set environment for LiteLLMos.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEYos.environ["OPENROUTER_API_BASE"] = OPENROUTER_BASE_URLresponse = completion(    model="openrouter/google/palm-2-chat-bison",    messages=messages,    base_url=OPENROUTER_BASE_URL  # Explicitly pass base_url for clarity)
```

This approach provides better flexibility for managing configurations across different environments (dev, staging, production) and makes it easier to switch between self-hosted and cloud endpoints.

## OpenRouter Completion Models

🚨 LiteLLM supports ALL OpenRouter models, send `model=openrouter/<your-openrouter-model>` to send it to open router. See all openrouter models [here](https://openrouter.ai/models)

| Model Name                              | Function Call                                                     |
| --------------------------------------- | ----------------------------------------------------------------- |
| openrouter/openai/gpt-3.5-turbo         | `completion('openrouter/openai/gpt-3.5-turbo', messages)`         |
| openrouter/openai/gpt-3.5-turbo-16k     | `completion('openrouter/openai/gpt-3.5-turbo-16k', messages)`     |
| openrouter/openai/gpt-4                 | `completion('openrouter/openai/gpt-4', messages)`                 |
| openrouter/openai/gpt-4-32k             | `completion('openrouter/openai/gpt-4-32k', messages)`             |
| openrouter/anthropic/claude-2           | `completion('openrouter/anthropic/claude-2', messages)`           |
| openrouter/anthropic/claude-instant-v1  | `completion('openrouter/anthropic/claude-instant-v1', messages)`  |
| openrouter/google/palm-2-chat-bison     | `completion('openrouter/google/palm-2-chat-bison', messages)`     |
| openrouter/google/palm-2-codechat-bison | `completion('openrouter/google/palm-2-codechat-bison', messages)` |
| openrouter/meta-llama/llama-2-13b-chat  | `completion('openrouter/meta-llama/llama-2-13b-chat', messages)`  |
| openrouter/meta-llama/llama-2-70b-chat  | `completion('openrouter/meta-llama/llama-2-70b-chat', messages)`  |

## Passing OpenRouter Params - transforms, models, route

Pass `transforms`, `models`, `route`as arguments to `litellm.completion()`

```
import osfrom litellm import completionos.environ["OPENROUTER_API_KEY"] = ""response = completion(            model="openrouter/google/palm-2-chat-bison",            messages=messages,            transforms = [""],            route= ""        )
```

## Embedding

```
from litellm import embeddingimport osos.environ["OPENROUTER_API_KEY"] = "your-api-key"response = embedding(    model="openrouter/openai/text-embedding-3-small",    input=["good morning from litellm", "this is another item"],)print(response)
```

## Image Generation

OpenRouter supports image generation through select models like Google Gemini image generation models. LiteLLM transforms standard image generation requests to OpenRouter's chat completion format.

### Supported Parameters

- `size`: Maps to OpenRouter's `aspect_ratio` format
  
  - `1024x1024` → `1:1` (square)
  - `1536x1024` → `3:2` (landscape)
  - `1024x1536` → `2:3` (portrait)
  - `1792x1024` → `16:9` (wide landscape)
  - `1024x1792` → `9:16` (tall portrait)

- `quality`: Maps to OpenRouter's `image_size` format (Gemini models)
  
  - `low` or `standard` → `1K`
  - `medium` → `2K`
  - `high` or `hd` → `4K`

- `n`: Number of images to generate

### Usage

```
from litellm import image_generationimport osos.environ["OPENROUTER_API_KEY"] = "your-api-key"# Basic image generationresponse = image_generation(    model="openrouter/google/gemini-2.5-flash-image",    prompt="A beautiful sunset over a calm ocean",)print(response)
```

### Advanced Usage with Parameters

```
from litellm import image_generationimport osos.environ["OPENROUTER_API_KEY"] = "your-api-key"# Generate high-quality landscape imageresponse = image_generation(    model="openrouter/google/gemini-2.5-flash-image",    prompt="A serene mountain landscape with a lake",    size="1536x1024",  # Landscape format    quality="high",     # High quality (4K))# Access the generated imageimage_data = response.data[0]if image_data.b64_json:    # Base64 encoded image    print(f"Generated base64 image: {image_data.b64_json[:50]}...")elif image_data.url:    # Image URL    print(f"Generated image URL: {image_data.url}")
```

### Using OpenRouter-Specific Parameters

You can also pass OpenRouter-specific parameters directly using `image_config`:

```
from litellm import image_generationimport osos.environ["OPENROUTER_API_KEY"] = "your-api-key"response = image_generation(    model="openrouter/google/gemini-2.5-flash-image",    prompt="A futuristic cityscape at night",    image_config={        "aspect_ratio": "16:9",  # OpenRouter native format        "image_size": "4K"       # OpenRouter native format    })print(response)
```

### Response Format

The response follows the standard LiteLLM ImageResponse format:

```
{    "created": 1703658209,    "data": [{        "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",  # Base64 encoded image        "url": None,        "revised_prompt": None    }],    "usage": {        "input_tokens": 10,        "output_tokens": 1290,        "total_tokens": 1300    }}
```

### Cost Tracking

OpenRouter provides cost information in the response, which LiteLLM automatically tracks:

```
response = image_generation(    model="openrouter/google/gemini-2.5-flash-image",    prompt="A cute baby sea otter",)# Cost is available in the response metadataprint(f"Request cost: ${response._hidden_params['additional_headers']['llm_provider-x-litellm-response-cost']}")
```

[

Previous

Ollama

](https://docs.litellm.ai/docs/providers/ollama)[  
](https://docs.litellm.ai/docs/providers/sarvam)


- [Supported Models & Providers](https://docs.litellm.ai/docs/providers)
- Anthropic

# Anthropic

LiteLLM supports all anthropic models.

- `claude-sonnet-4-5-20250929`
- `claude-opus-4-5-20251101`
- `claude-opus-4-1-20250805`
- `claude-4` (`claude-opus-4-20250514`, `claude-sonnet-4-20250514`)
- `claude-3.7` (`claude-3-7-sonnet-20250219`)
- `claude-3.5` (`claude-3-5-sonnet-20240620`)
- `claude-3` (`claude-3-haiku-20240307`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`)
- `claude-2`
- `claude-2.1`
- `claude-instant-1.2`

| Property                  | Details                                                                                                                                                                                                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description               | Claude is a highly performant, trustworthy, and intelligent AI platform built by Anthropic. Claude excels at tasks involving language, reasoning, analysis, coding, and more. Also available via Azure Foundry.                                                                             |
| Provider Route on LiteLLM | `anthropic/` (add this prefix to the model name, to route any requests to Anthropic - e.g. `anthropic/claude-3-5-sonnet-20240620`). For Azure Foundry deployments, use `azure/claude-*` (see [Azure Anthropic documentation](https://docs.litellm.ai/docs/providers/azure/azure_anthropic)) |
| Provider Doc              | [Anthropic ↗](https://docs.anthropic.com/en/docs/build-with-claude/overview), [Azure Foundry Claude ↗](https://learn.microsoft.com/en-us/azure/ai-services/foundry-models/claude)                                                                                                           |
| API Endpoint for Provider | [https://api.anthropic.com](https://api.anthropic.com/) (or Azure Foundry endpoint: `https://<resource-name>.services.ai.azure.com/anthropic`)                                                                                                                                              |
| Supported Endpoints       | `/chat/completions`, `/v1/messages` (passthrough)                                                                                                                                                                                                                                           |

## Supported OpenAI Parameters

Check this in code, [here](https://docs.litellm.ai/docs/completion/input#translated-openai-params)

```
"stream","stop","temperature","top_p","max_tokens","max_completion_tokens","tools","tool_choice","extra_headers","parallel_tool_calls","response_format","user","reasoning_effort",
```

info

**Notes:**

- Anthropic API fails requests when `max_tokens` are not passed. Due to this litellm passes `max_tokens=4096` when no `max_tokens` are passed.
- `response_format` is fully supported for Claude Sonnet 4.5 and Opus 4.1 models (see [Structured Outputs](https://docs.litellm.ai/docs/providers/anthropic#structured-outputs) section)
- `reasoning_effort` is automatically mapped to `output_config={"effort": ...}` for Claude Opus 4.5 models (see [Effort Parameter](https://docs.litellm.ai/docs/providers/anthropic_effort))

## **Structured Outputs**

LiteLLM supports Anthropic's [structured outputs feature](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) for Claude Sonnet 4.5 and Opus 4.1 models. When you use `response_format` with these models, LiteLLM automatically:

- Adds the required `structured-outputs-2025-11-13` beta header
- Transforms OpenAI's `response_format` to Anthropic's `output_format` format

### Supported Models

- `sonnet-4-5` or `sonnet-4.5` (all Sonnet 4.5 variants)
- `opus-4-1` or `opus-4.1` (all Opus 4.1 variants)
  - `opus-4-5` or `opus-4.5` (all Opus 4.5 variants)

### Example Usage

- LiteLLM SDK
- LiteLLM Proxy

```
from litellm import completionresponse = completion(    model="claude-sonnet-4-5-20250929",    messages=[{"role": "user", "content": "What is the capital of France?"}],    response_format={        "type": "json_schema",        "json_schema": {            "name": "capital_response",            "strict": True,            "schema": {                "type": "object",                "properties": {                    "country": {"type": "string"},                    "capital": {"type": "string"}                },                "required": ["country", "capital"],                "additionalProperties": False            }        }    })print(response.choices[0].message.content)# Output: {"country": "France", "capital": "Paris"}
```

info

When using structured outputs with supported models, LiteLLM automatically:

- Converts OpenAI's `response_format` to Anthropic's `output_schema`
- Adds the `anthropic-beta: structured-outputs-2025-11-13` header
- Creates a tool with the schema and forces the model to use it

## API Keys

```
import osos.environ["ANTHROPIC_API_KEY"] = "your-api-key"# os.environ["ANTHROPIC_API_BASE"] = "" # [OPTIONAL] or 'ANTHROPIC_BASE_URL'# os.environ["LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX"] = "true" # [OPTIONAL] Disable automatic URL suffix appending
```

Azure Foundry Support

Claude models are also available via Microsoft Azure Foundry. Use the `azure/` prefix instead of `anthropic/` and configure Azure authentication. See the [Azure Anthropic documentation](https://docs.litellm.ai/docs/providers/azure/azure_anthropic) for details.

Example:

```
response = completion(    model="azure/claude-sonnet-4-5",    api_base="https://<resource-name>.services.ai.azure.com/anthropic",    api_key="your-azure-api-key",    messages=[{"role": "user", "content": "Hello!"}])
```

### Custom API Base

When using a custom API base for Anthropic (e.g., a proxy or custom endpoint), LiteLLM automatically appends the appropriate suffix (`/v1/messages` or `/v1/complete`) to your base URL.

If your custom endpoint already includes the full path or doesn't follow Anthropic's standard URL structure, you can disable this automatic suffix appending:

```
import osos.environ["ANTHROPIC_API_BASE"] = "https://my-custom-endpoint.com/custom/path"os.environ["LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX"] = "true"  # Prevents automatic suffix
```

Without `LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX`:

- Base URL `https://my-proxy.com` → `https://my-proxy.com/v1/messages`
- Base URL `https://my-proxy.com/api` → `https://my-proxy.com/api/v1/messages`

With `LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX=true`:

- Base URL `https://my-proxy.com/custom/path` → `https://my-proxy.com/custom/path` (unchanged)

### Azure AI Foundry (Alternative Method)

Recommended Method

For full Azure support including Azure AD authentication, use the dedicated [Azure Anthropic provider](https://docs.litellm.ai/docs/providers/azure/azure_anthropic) with `azure_ai/` prefix.

As an alternative, you can use the `anthropic/` provider directly with your Azure endpoint since Azure exposes Claude using Anthropic's native API.

```
from litellm import completionresponse = completion(    model="anthropic/claude-sonnet-4-5",    api_base="https://<your-resource>.services.ai.azure.com/anthropic",    api_key="<your-azure-api-key>",    messages=[{"role": "user", "content": "Hello!"}],)print(response)
```

info

**Finding your Azure endpoint:** Go to Azure AI Foundry → Your deployment → Overview. Your base URL will be `https://<resource-name>.services.ai.azure.com/anthropic`

## Usage

```
import osfrom litellm import completion# set env - [OPTIONAL] replace with your anthropic keyos.environ["ANTHROPIC_API_KEY"] = "your-api-key"messages = [{"role": "user", "content": "Hey! how's it going?"}]response = completion(model="claude-opus-4-20250514", messages=messages)print(response)
```

## Usage - Streaming

Just set `stream=True` when calling completion.

```
import osfrom litellm import completion# set envos.environ["ANTHROPIC_API_KEY"] = "your-api-key"messages = [{"role": "user", "content": "Hey! how's it going?"}]response = completion(model="claude-opus-4-20250514", messages=messages, stream=True)for chunk in response:    print(chunk["choices"][0]["delta"]["content"])  # same as openai format
```

## Usage with LiteLLM Proxy

Here's how to call Anthropic with the LiteLLM Proxy Server

### 1. Save key in your environment

```
export ANTHROPIC_API_KEY="your-api-key"
```

### 2. Start the proxy

- config.yaml
- config - default all Anthropic Model
- cli

```
model_list:  - model_name: claude-4 ### RECEIVED MODEL NAME ###    litellm_params: # all params accepted by litellm.completion() - https://docs.litellm.ai/docs/completion/input      model: claude-opus-4-20250514 ### MODEL NAME sent to `litellm.completion()` ###      api_key: "os.environ/ANTHROPIC_API_KEY" # does os.getenv("ANTHROPIC_API_KEY")
```

```
litellm --config /path/to/config.yaml
```

### 3. Test it

- Curl Request
- OpenAI v1.0.0+
- Langchain

```
curl --location 'http://0.0.0.0:4000/chat/completions' \--header 'Content-Type: application/json' \--data ' {      "model": "claude-3",      "messages": [        {          "role": "user",          "content": "what llm are you"        }      ]    }'
```

## Supported Models

`Model Name` 👉 Human-friendly name.  
`Function Call` 👉 How to call the model in LiteLLM.

| Model Name                 | Function Call                                        |
| -------------------------- | ---------------------------------------------------- |
| claude-sonnet-4-5          | `completion('claude-sonnet-4-5-20250929', messages)` |
| claude-opus-4              | `completion('claude-opus-4-20250514', messages)`     |
| claude-sonnet-4            | `completion('claude-sonnet-4-20250514', messages)`   |
| claude-3.7                 | `completion('claude-3-7-sonnet-20250219', messages)` |
| claude-3-5-sonnet          | `completion('claude-3-5-sonnet-20240620', messages)` |
| claude-3-haiku             | `completion('claude-3-haiku-20240307', messages)`    |
| claude-3-opus              | `completion('claude-3-opus-20240229', messages)`     |
| claude-3-5-sonnet-20240620 | `completion('claude-3-5-sonnet-20240620', messages)` |
| claude-3-sonnet            | `completion('claude-3-sonnet-20240229', messages)`   |
| claude-2.1                 | `completion('claude-2.1', messages)`                 |
| claude-2                   | `completion('claude-2', messages)`                   |
| claude-instant-1.2         | `completion('claude-instant-1.2', messages)`         |
| claude-instant-1           | `completion('claude-instant-1', messages)`           |

## **Prompt Caching**

Use Anthropic Prompt Caching

[Relevant Anthropic API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

note

Here's what a sample Raw Request from LiteLLM for Anthropic Context Caching looks like:

```
POST Request Sent from LiteLLM:curl -X POST \https://api.anthropic.com/v1/messages \-H 'accept: application/json' -H 'anthropic-version: 2023-06-01' -H 'content-type: application/json' -H 'x-api-key: sk-...' \-d '{'model': 'claude-3-5-sonnet-20240620', [    {      "role": "user",      "content": [        {          "type": "text",          "text": "What are the key terms and conditions in this agreement?",          "cache_control": {            "type": "ephemeral"          }        }      ]    },    {      "role": "assistant",      "content": [        {          "type": "text",          "text": "Certainly! The key terms and conditions are the following: the contract is 1 year long for $10/mo"        }      ]    }  ],  "temperature": 0.2,  "max_tokens": 10}'
```

**Note:** Anthropic no longer requires the `anthropic-beta: prompt-caching-2024-07-31` header. Prompt caching now works automatically when you use `cache_control` in your messages.

### Caching - Large Context Caching

This example demonstrates basic Prompt Caching usage, caching the full text of the legal agreement as a prefix while keeping the user instruction uncached.

- LiteLLM SDK
- LiteLLM Proxy

```
response = await litellm.acompletion(    model="anthropic/claude-3-5-sonnet-20240620",    messages=[        {            "role": "system",            "content": [                {                    "type": "text",                    "text": "You are an AI assistant tasked with analyzing legal documents.",                },                {                    "type": "text",                    "text": "Here is the full text of a complex legal agreement",                    "cache_control": {"type": "ephemeral"},                },            ],        },        {            "role": "user",            "content": "what are the key terms and conditions in this agreement?",        },    ])
```

### Caching - Tools definitions

In this example, we demonstrate caching tool definitions.

The cache_control parameter is placed on the final tool

- LiteLLM SDK
- LiteLLM Proxy

```
import litellmresponse = await litellm.acompletion(    model="anthropic/claude-3-5-sonnet-20240620",    messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]    tools = [        {            "type": "function",            "function": {                "name": "get_current_weather",                "description": "Get the current weather in a given location",                "parameters": {                    "type": "object",                    "properties": {                        "location": {                            "type": "string",                            "description": "The city and state, e.g. San Francisco, CA",                        },                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},                    },                    "required": ["location"],                },                "cache_control": {"type": "ephemeral"}            },        }    ])
```

### Caching - Continuing Multi-Turn Convo

In this example, we demonstrate how to use Prompt Caching in a multi-turn conversation.

The cache_control parameter is placed on the system message to designate it as part of the static prefix.

The conversation history (previous messages) is included in the messages array. The final turn is marked with cache-control, for continuing in followups. The second-to-last user message is marked for caching with the cache_control parameter, so that this checkpoint can read from the previous cache.

- LiteLLM SDK
- LiteLLM Proxy

```
import litellmresponse = await litellm.acompletion(    model="anthropic/claude-3-5-sonnet-20240620",    messages=[        # System Message        {            "role": "system",            "content": [                {                    "type": "text",                    "text": "Here is the full text of a complex legal agreement"                    * 400,                    "cache_control": {"type": "ephemeral"},                }            ],        },        # marked for caching with the cache_control parameter, so that this checkpoint can read from the previous cache.        {            "role": "user",            "content": [                {                    "type": "text",                    "text": "What are the key terms and conditions in this agreement?",                    "cache_control": {"type": "ephemeral"},                }            ],        },        {            "role": "assistant",            "content": "Certainly! the key terms and conditions are the following: the contract is 1 year long for $10/mo",        },        # The final turn is marked with cache-control, for continuing in followups.        {            "role": "user",            "content": [                {                    "type": "text",                    "text": "What are the key terms and conditions in this agreement?",                    "cache_control": {"type": "ephemeral"},                }            ],        },    ])
```

## **Function/Tool Calling**

```
from litellm import completion# set envos.environ["ANTHROPIC_API_KEY"] = "your-api-key"tools = [    {        "type": "function",        "function": {            "name": "get_current_weather",            "description": "Get the current weather in a given location",            "parameters": {                "type": "object",                "properties": {                    "location": {                        "type": "string",                        "description": "The city and state, e.g. San Francisco, CA",                    },                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},                },                "required": ["location"],            },        },    }]messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]response = completion(    model="anthropic/claude-3-opus-20240229",    messages=messages,    tools=tools,    tool_choice="auto",)# Add any assertions, here to check response argsprint(response)assert isinstance(response.choices[0].message.tool_calls[0].function.name, str)assert isinstance(    response.choices[0].message.tool_calls[0].function.arguments, str)
```

### Forcing Anthropic Tool Use

If you want Claude to use a specific tool to answer the user’s question

You can do this by specifying the tool in the `tool_choice` field like so:

```
response = completion(    model="anthropic/claude-3-opus-20240229",    messages=messages,    tools=tools,    tool_choice={"type": "tool", "name": "get_weather"},)
```

### Disable Tool Calling

You can disable tool calling by setting the `tool_choice` to `"none"`.

- SDK
- Proxy

```
from litellm import completionresponse = completion(    model="anthropic/claude-3-opus-20240229",    messages=messages,    tools=tools,    tool_choice="none",)
```

### MCP Tool Calling

Here's how to use MCP tool calling with Anthropic:

- LiteLLM SDK
- LiteLLM Proxy

LiteLLM supports MCP tool calling with Anthropic in the OpenAI Responses API format.

- OpenAI Format
- Anthropic Format

```
import os from litellm import completionos.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."tools=[    {        "type": "mcp",        "server_label": "deepwiki",        "server_url": "https://mcp.deepwiki.com/mcp",        "require_approval": "never",    },]response = completion(    model="anthropic/claude-sonnet-4-20250514",    messages=[{"role": "user", "content": "Who won the World Cup in 2022?"}],    tools=tools)
```

### Parallel Function Calling

Here's how to pass the result of a function call back to an anthropic model:

```
from litellm import completionimport os os.environ["ANTHROPIC_API_KEY"] = "sk-ant.."litellm.set_verbose = True### 1ST FUNCTION CALL ###tools = [    {        "type": "function",        "function": {            "name": "get_current_weather",            "description": "Get the current weather in a given location",            "parameters": {                "type": "object",                "properties": {                    "location": {                        "type": "string",                        "description": "The city and state, e.g. San Francisco, CA",                    },                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},                },                "required": ["location"],            },        },    }]messages = [    {        "role": "user",        "content": "What's the weather like in Boston today in Fahrenheit?",    }]try:    # test without max tokens    response = completion(        model="anthropic/claude-3-opus-20240229",        messages=messages,        tools=tools,        tool_choice="auto",    )    # Add any assertions, here to check response args    print(response)    assert isinstance(response.choices[0].message.tool_calls[0].function.name, str)    assert isinstance(        response.choices[0].message.tool_calls[0].function.arguments, str    )    messages.append(        response.choices[0].message.model_dump()    )  # Add assistant tool invokes    tool_result = (        '{"location": "Boston", "temperature": "72", "unit": "fahrenheit"}'    )    # Add user submitted tool results in the OpenAI format    messages.append(        {            "tool_call_id": response.choices[0].message.tool_calls[0].id,            "role": "tool",            "name": response.choices[0].message.tool_calls[0].function.name,            "content": tool_result,        }    )    ### 2ND FUNCTION CALL ###    # In the second response, Claude should deduce answer from tool results    second_response = completion(        model="anthropic/claude-3-opus-20240229",        messages=messages,        tools=tools,        tool_choice="auto",    )    print(second_response)except Exception as e:    print(f"An error occurred - {str(e)}")
```

s/o @[Shekhar Patnaik](https://www.linkedin.com/in/patnaikshekhar) for requesting this!

### Context Management (Beta)

Anthropic’s [context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing) API lets you automatically clear older tool results or thinking blocks. LiteLLM now forwards the native `context_management` payload when you call Anthropic models, and automatically attaches the required `context-management-2025-06-27` beta header.

```
from litellm import completionresponse = completion(    model="anthropic/claude-sonnet-4-20250514",    messages=[{"role": "user", "content": "Summarize the latest tool results"}],    context_management={        "edits": [            {                "type": "clear_tool_uses_20250919",                "trigger": {"type": "input_tokens", "value": 30000},                "keep": {"type": "tool_uses", "value": 3},                "clear_at_least": {"type": "input_tokens", "value": 5000},                "exclude_tools": ["web_search"],            }        ]    },)
```

### Anthropic Hosted Tools (Computer, Text Editor, Web Search, Memory)

- Computer
- Text Editor
- Web Search
- Memory

```
from litellm import completiontools = [    {        "type": "computer_20241022",        "function": {            "name": "computer",            "parameters": {                "display_height_px": 100,                "display_width_px": 100,                "display_number": 1,            },        },    }]model = "claude-3-5-sonnet-20241022"messages = [{"role": "user", "content": "Save a picture of a cat to my desktop."}]resp = completion(    model=model,    messages=messages,    tools=tools,    # headers={"anthropic-beta": "computer-use-2024-10-22"},)print(resp)
```

## Usage - Vision

```
from litellm import completion# set envos.environ["ANTHROPIC_API_KEY"] = "your-api-key"def encode_image(image_path):    import base64    with open(image_path, "rb") as image_file:        return base64.b64encode(image_file.read()).decode("utf-8")image_path = "../proxy/cached_logo.jpg"# Getting the base64 stringbase64_image = encode_image(image_path)resp = litellm.completion(    model="anthropic/claude-3-opus-20240229",    messages=[        {            "role": "user",            "content": [                {"type": "text", "text": "Whats in this image?"},                {                    "type": "image_url",                    "image_url": {                        "url": "data:image/jpeg;base64," + base64_image                    },                },            ],        }    ],)print(f"\nResponse: {resp}")
```

## Usage - Thinking / `reasoning_content`

LiteLLM translates OpenAI's `reasoning_effort` to Anthropic's `thinking` parameter. [Code](https://github.com/BerriAI/litellm/blob/23051d89dd3611a81617d84277059cd88b2df511/litellm/llms/anthropic/chat/transformation.py#L298)

| reasoning_effort | thinking              |
| ---------------- | --------------------- |
| "low"            | "budget_tokens": 1024 |
| "medium"         | "budget_tokens": 2048 |
| "high"           | "budget_tokens": 4096 |

- SDK
- PROXY

```
from litellm import completionresp = completion(    model="anthropic/claude-3-7-sonnet-20250219",    messages=[{"role": "user", "content": "What is the capital of France?"}],    reasoning_effort="low",)
```

**Expected Response**

```
ModelResponse(    id='chatcmpl-c542d76d-f675-4e87-8e5f-05855f5d0f5e',    created=1740470510,    model='claude-3-7-sonnet-20250219',    object='chat.completion',    system_fingerprint=None,    choices=[        Choices(            finish_reason='stop',            index=0,            message=Message(                content="The capital of France is Paris.",                role='assistant',                tool_calls=None,                function_call=None,                provider_specific_fields={                    'citations': None,                    'thinking_blocks': [                        {                            'type': 'thinking',                            'thinking': 'The capital of France is Paris. This is a very straightforward factual question.',                            'signature': 'EuYBCkQYAiJAy6...'                        }                    ]                }            ),            thinking_blocks=[                {                    'type': 'thinking',                    'thinking': 'The capital of France is Paris. This is a very straightforward factual question.',                    'signature': 'EuYBCkQYAiJAy6AGB...'                }            ],            reasoning_content='The capital of France is Paris. This is a very straightforward factual question.'        )    ],    usage=Usage(        completion_tokens=68,        prompt_tokens=42,        total_tokens=110,        completion_tokens_details=None,        prompt_tokens_details=PromptTokensDetailsWrapper(            audio_tokens=None,            cached_tokens=0,            text_tokens=None,            image_tokens=None        ),        cache_creation_input_tokens=0,        cache_read_input_tokens=0    ))
```

### Pass `thinking` to Anthropic models

You can also pass the `thinking` parameter to Anthropic models.

You can also pass the `thinking` parameter to Anthropic models.

- SDK
- PROXY

```
response = litellm.completion(  model="anthropic/claude-3-7-sonnet-20250219",  messages=[{"role": "user", "content": "What is the capital of France?"}],  thinking={"type": "enabled", "budget_tokens": 1024},)
```

## **Passing Extra Headers to Anthropic API**

Pass `extra_headers: dict` to `litellm.completion`

```
from litellm import completionmessages = [{"role": "user", "content": "What is Anthropic?"}]response = completion(    model="claude-3-5-sonnet-20240620",     messages=messages,     extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"})
```

## Usage - "Assistant Pre-fill"

You can "put words in Claude's mouth" by including an `assistant` role message as the last item in the `messages` array.

> [!IMPORTANT] The returned completion will *not* include your "pre-fill" text, since it is part of the prompt itself. Make sure to prefix Claude's completion with your pre-fill.

```
import osfrom litellm import completion# set env - [OPTIONAL] replace with your anthropic keyos.environ["ANTHROPIC_API_KEY"] = "your-api-key"messages = [    {"role": "user", "content": "How do you say 'Hello' in German? Return your answer as a JSON object, like this:\n\n{ \"Hello\": \"Hallo\" }"},    {"role": "assistant", "content": "{"},]response = completion(model="claude-2.1", messages=messages)print(response)
```

#### Example prompt sent to Claude

```
Human: How do you say 'Hello' in German? Return your answer as a JSON object, like this:{ "Hello": "Hallo" }Assistant: {
```

## Usage - "System" messages

If you're using Anthropic's Claude 2.1, `system` role messages are properly formatted for you.

```
import osfrom litellm import completion# set env - [OPTIONAL] replace with your anthropic keyos.environ["ANTHROPIC_API_KEY"] = "your-api-key"messages = [    {"role": "system", "content": "You are a snarky assistant."},    {"role": "user", "content": "How do I boil water?"},]response = completion(model="claude-2.1", messages=messages)
```

#### Example prompt sent to Claude

```
You are a snarky assistant.Human: How do I boil water?Assistant:
```

## Usage - PDF

Pass base64 encoded PDF files to Anthropic models using the `file` content type with a `file_data` field.

- SDK
- PROXY

### **using base64**

```
from litellm import completion, supports_pdf_inputimport base64import requests# URL of the fileurl = "https://storage.googleapis.com/cloud-samples-data/generative-ai/pdf/2403.05530.pdf"# Download the fileresponse = requests.get(url)file_data = response.contentencoded_file = base64.b64encode(file_data).decode("utf-8")## check if model supports pdf input - (2024/11/11) only claude-3-5-haiku-20241022 supports itsupports_pdf_input("anthropic/claude-3-5-haiku-20241022") # Trueresponse = completion(    model="anthropic/claude-3-5-haiku-20241022",    messages=[        {            "role": "user",            "content": [                {"type": "text", "text": "You are a very professional document summarization specialist. Please summarize the given document."},                {                    "type": "file",                    "file": {                       "file_data": f"data:application/pdf;base64,{encoded_file}", # 👈 PDF                    }                },            ],        }    ],    max_tokens=300,)print(response.choices[0])
```

## [BETA] Citations API

Pass `citations: {"enabled": true}` to Anthropic, to get citations on your document responses.

Note: This interface is in BETA. If you have feedback on how citations should be returned, please [tell us here](https://github.com/BerriAI/litellm/issues/7970#issuecomment-2644437943)

- SDK
- PROXY

```
from litellm import completionresp = completion(    model="claude-3-5-sonnet-20241022",    messages=[        {            "role": "user",            "content": [                {                    "type": "document",                    "source": {                        "type": "text",                        "media_type": "text/plain",                        "data": "The grass is green. The sky is blue.",                    },                    "title": "My Document",                    "context": "This is a trustworthy document.",                    "citations": {"enabled": True},                },                {                    "type": "text",                    "text": "What color is the grass and sky?",                },            ],        }    ],)citations = resp.choices[0].message.provider_specific_fields["citations"]assert citations is not None
```

## Usage - passing 'user_id' to Anthropic

LiteLLM translates the OpenAI `user` param to Anthropic's `metadata[user_id]` param.

- SDK
- PROXY

```
response = completion(    model="claude-3-5-sonnet-20240620",    messages=messages,    user="user_123",)
```

## Usage - Agent Skills

LiteLLM supports using Agent Skills with the API

- SDK
- PROXY

```
response = completion(    model="claude-sonnet-4-5-20250929",    messages=messages,    tools= [        {            "type": "code_execution_20250825",            "name": "code_execution"        }    ],    container= {        "skills": [            {                "type": "anthropic",                "skill_id": "pptx",                "version": "latest"            }        ]    })
```

The container and its "id" will be present in "provider_specific_fields" in streaming/non-streaming response

