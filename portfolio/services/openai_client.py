import os

from openai import OpenAI


class OpenAIConfigurationError(Exception):
    """Raised when OpenAI API configuration is missing."""


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise OpenAIConfigurationError(
            "OPENAI_API_KEY is missing. Configure it in your local .env file."
        )

    return OpenAI(
        api_key=api_key,
        timeout=30.0,
        max_retries=2,
    )


def generate_text(prompt: str) -> str:
    prompt = prompt.strip()

    if not prompt:
        raise ValueError("Prompt cannot be empty.")

    model = os.getenv("OPENAI_MODEL", "ChatGPT 6 Astra").strip()

    if not model:
        raise OpenAIConfigurationError("OPENAI_MODEL is missing.")

    client = get_openai_client()

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text
