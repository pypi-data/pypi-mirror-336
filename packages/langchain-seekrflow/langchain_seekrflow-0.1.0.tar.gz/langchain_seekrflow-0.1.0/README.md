# langchain-seekrflow

**langchain-seekrflow** is an open-source integration package that wraps SeekrFlow’s chat model endpoints for seamless use with LangChain. This package provides a simple interface—via the `ChatSeekrFlow` class—to incorporate SeekrFlow's AI-powered chat models into your LangChain applications.

> **Note:** This integration package is maintained independently from the core LangChain repository. Documentation for LangChain integrations continues to be maintained in the LangChain docs.

---

## Features

- **LangChain Compatibility:** Implements the LangChain `BaseChatModel` interface.
- **Streaming Support:** Enables token-level streaming of responses.
- **Flexible Input Handling:** Accepts strings, lists of messages, or dictionary inputs.
- **Easy Integration:** Designed to work seamlessly with other LangChain components such as prompt templates and chain runners.

---

## Installation

Ensure you have Python 3.10 (or compatible) installed. Then install via [Poetry](https://python-poetry.org/) or pip:

### Using pip (if published to PyPI)
```bash
pip install langchain-seekrflow
```

### Using Poetry
Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/langchain-seekrflow.git
cd langchain-seekrflow
poetry install
```

---

## Usage

Below is a quick example demonstrating how to use `ChatSeekrFlow`:

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_core.runnables import RunnableSequence
from langchain_seekrflow import ChatSeekrFlow
from seekrai import SeekrFlow

# Set your Seekr API key
SEEKR_API_KEY = "your-api-key-here"

# Initialize the SeekrFlow client (from seekrai)
seekr_client = SeekrFlow(api_key=SEEKR_API_KEY)

# Instantiate the ChatSeekrFlow model (for non-streaming mode)
llm = ChatSeekrFlow(
    client=seekr_client, 
    model_name="meta-llama/Meta-Llama-3-8B-Instruct"
)

# Synchronous invocation example:
response = llm.invoke([HumanMessage(content="Hello, Seekr!")])
print("Response:", response.content)

# Chaining example:
prompt = ChatPromptTemplate.from_template("Translate to French: {text}")
chain: RunnableSequence = prompt | llm
result = chain.invoke({"text": "Good morning"})
print("Chained response:", result)

# Streaming example:
llm.streaming = True  # Enable streaming
for chunk in llm.stream([HumanMessage(content="Write me a haiku.")]):
    print(chunk.content, end="", flush=True)
```

---

## Configuration & Requirements

- **API Key:** You must have a valid Seekr API key to authenticate requests. Set it as an environment variable or pass it to the `SeekrFlow` client.
- **Model Endpoint:** Ensure your model endpoint is compatible with OpenAI’s chat format. `ChatSeekrFlow` can be used with both fine-tuned and custom SeekrFlow models.
- **Dependencies:** This package depends on `langchain`, `seekrai`, and other libraries specified in the `pyproject.toml`.

---

## Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/benfaircloth/langchain-seekrflow) to help improve the package. For guidelines, see our [Contributing Guide](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## API Reference

LangChain maintains documentation for community integrations separately. Once this integration is added to their docs, you’ll be able to find `ChatSeekrFlow` in the [LangChain integrations section](https://python.langchain.com/docs/integrations/).

> Until then, refer to this repo’s code and examples for usage.

---

Happy coding!