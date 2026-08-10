def execute_action(
    intent,
    user_message,
    vehicle_state,
    emotion_profile=None
):
    """
    Execute a vehicle action based on the detected intent.

    Returns:
        The assistant's confirmation message.
    """

    if intent == "play_music":
        vehicle_state["music_status"] = "Playing"

        if emotion_profile:
            music_category = emotion_profile["music_category"]
        else:
            music_category = "default"

        vehicle_state["music_category"] = music_category.title()

        return f"Playing {music_category} music."

    if intent == "navigate_home":
        vehicle_state["destination"] = "Home"
        vehicle_state["navigation_active"] = True

        return "Starting navigation to Home."

    if intent == "set_temperature":
        words = user_message.split()

        for word in words:
            if word.isdigit():
                temperature = int(word)
                vehicle_state["temperature"] = temperature

                return f"Setting the temperature to {temperature}°C."

        return "Please tell me what temperature you would like."

    return "I received your request."

def execute_structured_action(
    command,
    vehicle_state,
    emotion_profile=None
):
    """
    Execute a structured command produced by the language model.
    """

    intent = command.get("intent")
    if intent == "conversation":
        return "No vehicle action was performed."

    if intent == "play_music":
        vehicle_state["music_status"] = "Playing"

        if emotion_profile:
            music_category = emotion_profile["music_category"]
        else:
            music_category = "default"

        vehicle_state["music_category"] = music_category.title()

        return f"Playing {music_category} music."

    if intent == "set_temperature":
        temperature = command.get("temperature")

        if isinstance(temperature, (int, float)):
            vehicle_state["temperature"] = temperature

            return (
                f"Temperature set to "
                f"{temperature}°C."
            )

        return "I need a specific temperature."

    if intent == "adjust_temperature":
        direction = command.get("direction")

        if direction == "increase":
            vehicle_state["temperature"] += 2

            return (
                f"Temperature increased to "
                f"{vehicle_state['temperature']}°C."
            )

        if direction == "decrease":
            vehicle_state["temperature"] -= 2

            return (
                f"Temperature decreased to "
                f"{vehicle_state['temperature']}°C."
            )

        return "I couldn't determine how to adjust the temperature."

    if intent == "navigate_home":
        vehicle_state["destination"] = "Home"
        vehicle_state["navigation_active"] = True

        return "Starting navigation to Home."

    return "I couldn't identify a vehicle action."