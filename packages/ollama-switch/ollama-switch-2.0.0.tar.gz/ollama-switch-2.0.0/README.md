# Ollama Manager

A Python package to manage Ollama service and models.

## Installation

To install the package, run:

```bash
pip install ollama_manager
```

## Usage

Here are some examples of how to use the Ollama Manager:

### Starting the Service

```python
from ollama_manager import OllamaService

OllamaService.start_service()
```

### Stopping the Service

```python
from ollama_manager import OllamaService

OllamaService.stop_service()
```

### Loading a Model

```python
from ollama_manager import OllamaService

model = "gemma3:1b"
OllamaService.load(model)
```

### Unloading a Model

```python
from ollama_manager import OllamaService

model = "gemma3:1b"
OllamaService.unload(model)
```

### Streaming a Response

```python
from ollama_manager import OllamaService

model = "gemma3:1b"
messages = [{"role": "user", "content": "What is math?"}]
OllamaService.stream_response(model, messages)
```

For more detailed usage, refer to the `OllamaManager.py` file in the `src/ollama_manager` directory.

### Console Chat On/Off

```python
from ollama_manager import OllamaService

model = "deepseek-r1:32b"
system_message = "You are a helpful assistant."
OllamaService.console_chat_on_off(model, system_message)
```

This method allows for interactive chat with the Ollama service. It starts the service manually, loads the specified model, and enables a console-based chat interface where users can input questions and receive responses. The chat continues until the user types 'quit' to exit. After the chat session, the method unloads the model and stops the service manually.
