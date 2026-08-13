import json

from src.llm.ollama_client import generate_response


def parse_command(
    user_message,
    vehicle_state,
    conversation_history=None
):
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

7. cancel_navigation

Use this when the user wants to stop or cancel the currently active navigation.

Schema:
{
  "intent": "cancel_navigation"
}

Examples:

User: "Cancel navigation"
Output:
{"intent": "cancel_navigation"}

User: "Stop navigation"
Output:
{"intent": "cancel_navigation"}

User: "Cancel that"
Output:
{"intent": "cancel_navigation"}

User: "Stop the route"
Output:
{"intent": "cancel_navigation"}

8. pause_music

Use this when the user wants to stop or pause currently playing music.

Schema:
{
  "intent": "pause_music"
}

Examples:

User: "Pause the music"
Output:
{"intent": "pause_music"}

User: "Stop the music"
Output:
{"intent": "pause_music"}

User: "Turn that off"
Output:
{"intent": "pause_music"}

User: "Pause it"
Output:
{"intent": "pause_music"}

9. resume_music

Use this when the user wants to resume previously paused music.

Schema:
{
  "intent": "resume_music"
}

Examples:

User: "Resume the music"
Output:
{"intent": "resume_music"}

User: "Continue the music"
Output:
{"intent": "resume_music"}

User: "Play it again"
Output:
{"intent": "resume_music"}

User: "Resume it"
Output:
{"intent": "resume_music"}

10. navigate_to

Use this when the user asks to navigate to a specific destination other than Home.

Schema:
{
  "intent": "navigate_to",
  "destination": "University of Birmingham"
}

Examples:

User: "Navigate to the University of Birmingham"
Output:
{"intent": "navigate_to", "destination": "University of Birmingham"}

User: "Take me to New Street Station"
Output:
{"intent": "navigate_to", "destination": "New Street Station"}

User: "Give me directions to Tesco"
Output:
{"intent": "navigate_to", "destination": "Tesco"}

User: "Drive to the airport"
Output:
{"intent": "navigate_to", "destination": "the airport"}

Rules:
- Extract only the destination requested by the user.
- Do not invent a destination.
- If the destination is Home, use the navigate_home intent instead.

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

CONVERSATIONAL FOLLOW-UP RULES:

A short reply such as:
- "yes"
- "sure"
- "okay"
- "go ahead"
- "do that"
- "please do"

may refer to a vehicle action suggested in the immediately preceding assistant message.

Only infer the action when the previous assistant message clearly offered a specific vehicle action.

Examples:

Assistant: "Would you like me to play some calming music?"
User: "Yes"
Output:
{"intent": "play_music"}

Assistant: "Would you like me to make the cabin warmer?"
User: "Go ahead"
Output:
{"intent": "adjust_temperature", "direction": "increase"}

Assistant: "Would you like me to navigate home?"
User: "Sure"
Output:
{"intent": "navigate_home"}

If navigation is currently active, phrases such as:
- "cancel that"
- "stop that"
- "cancel it"
- "stop navigation"
- "end the route"

should be interpreted as:
{"intent": "cancel_navigation"}

If music is currently playing, phrases such as:
- "pause it"
- "stop that"
- "turn that off"
- "stop the music"
- "pause the music"

should be interpreted as:
{"intent": "pause_music"}

If music is currently paused and a music category has already been selected,
phrases such as:
- "resume it"
- "continue it"
- "play it again"
- "continue the music"

should be interpreted as:
{"intent": "resume_music"}

If there is no clear previous vehicle-action suggestion, treat a reply such as
"yes" or "okay" as conversation.
"""
    if conversation_history is None:
        conversation_history = []

    recent_history = conversation_history[-4:]

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for message in recent_history:
        messages.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    messages.append(
        {
            "role": "user",
            "content": (
                f"Current vehicle temperature: "
                f"{vehicle_state['temperature']}°C\n\n"
                f"Current music status: "
                f"{vehicle_state['music_status']}\n\n"
                f"Current music category: "
                f"{vehicle_state['music_category']}\n\n"
                f"Current destination: "
                f"{vehicle_state['destination']}\n\n"
                f"User message: {user_message}"
            )
        }
    )

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