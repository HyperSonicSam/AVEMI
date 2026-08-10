from ollama import Client


MODEL_NAME = "qwen3:4b-instruct"

client = Client(
    host="http://localhost:11434"
)


def generate_response(messages, response_format=None):
    """
    Generate a response using the local Ollama model.
    """

    response = client.chat(
        model=MODEL_NAME,
        messages=messages,
        format=response_format
    )

    return response["message"]["content"]