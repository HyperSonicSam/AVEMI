import json

from src.llm.ollama_client import generate_response


def parse_command(user_message, vehicle_state):
    """
    Convert a natural-language user message into a structured vehicle command.

    The language model is used only to interpret the request.
    It does not directly modify the vehicle state.

    Returns:
        dict: Structured command if parsing succeeds.
        None: If the model does not return valid JSON.
    """

    system_prompt = """
You are a command parser for an in-vehicle conversational assistant.

Your job is to convert the user's message into exactly ONE structured JSON object.

Return JSON only.
Do not include explanations.
Do not include Markdown.
Do not include code fences.
Do not include any text before or after the JSON.

Supported intents:

1. conversation

Use this when the user is only talking, expressing an emotion,
making a statement, or asking something that does not require
a vehicle action.

Schema:
{
  "intent": "conversation"
}

Examples:

User: "I am stressed"
Output:
{"intent": "conversation"}

User: "I am having a bad day"
Output:
{"intent": "conversation"}

User: "Hello"
Output:
{"intent": "conversation"}


2. play_music

Use this when the user requests music or audio playback.

Schema:
{
  "intent": "play_music"
}

Examples:

User: "Play some music"
Output:
{"intent": "play_music"}

User: "Put something on"
Output:
{"intent": "play_music"}

User: "I am stressed, play something relaxing"
Output:
{"intent": "play_music"}


3. set_temperature

Use this when the user specifies an exact temperature.

Schema:
{
  "intent": "set_temperature",
  "temperature": 22
}

Examples:

User: "Set the temperature to 25"
Output:
{"intent": "set_temperature", "temperature": 25}

User: "Make it 19 degrees"
Output:
{"intent": "set_temperature", "temperature": 19}


4. adjust_temperature

Use this when the user clearly wants the cabin temperature
increased or decreased but does not give an exact temperature.

Increase schema:
{
  "intent": "adjust_temperature",
  "direction": "increase"
}

Decrease schema:
{
  "intent": "adjust_temperature",
  "direction": "decrease"
}

Examples:

User: "It is cold in here"
Output:
{"intent": "adjust_temperature", "direction": "increase"}

User: "I'm freezing"
Output:
{"intent": "adjust_temperature", "direction": "increase"}

User: "Make it warmer"
Output:
{"intent": "adjust_temperature", "direction": "increase"}

User: "It's too hot"
Output:
{"intent": "adjust_temperature", "direction": "decrease"}

User: "Make it cooler"
Output:
{"intent": "adjust_temperature", "direction": "decrease"}


5. navigate_home

Use this when the user asks to navigate to Home.

Schema:
{
  "intent": "navigate_home"
}

Examples:

User: "Take me home"
Output:
{"intent": "navigate_home"}

User: "Navigate home"
Output:
{"intent": "navigate_home"}

User: "Give me directions home"
Output:
{"intent": "navigate_home"}


6. unknown

Use this only when the request cannot reasonably be classified
as conversation or one of the supported vehicle actions.

Schema:
{
  "intent": "unknown"
}


IMPORTANT RULES:

- Do not perform a vehicle action just because the user mentions an emotion.
- "I am stressed" is conversation.
- "I am tired" is conversation.
- "I am sad" is conversation.
- "I am angry" is conversation.

- An emotional statement combined with an explicit vehicle request
  should use the appropriate vehicle intent.

Example:
User: "I am stressed, play some music"
Output:
{"intent": "play_music"}

- Only infer a temperature adjustment when the user's statement clearly
  refers to thermal comfort.

Example:
User: "I am cold"
Output:
{"intent": "adjust_temperature", "direction": "increase"}

- Do not invent exact temperature values when none were provided.
- Do not invent destinations.
- Do not claim to execute actions.
- Your only task is classification and extraction.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": (
                f"Current vehicle temperature: "
                f"{vehicle_state['temperature']}°C\n\n"
                f"User message: {user_message}"
            )
        }
    ]

    response = generate_response(
        messages,
        response_format="json"
    )

    try:
        command = json.loads(response)

    except json.JSONDecodeError:
        return None

    if not isinstance(command, dict):
        return None

    if "intent" not in command:
        return None

    return command