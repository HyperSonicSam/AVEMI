def execute_action(intent, user_message, vehicle_state):
    """
    Execute a vehicle action based on the detected intent.

    Returns:
        The assistant's confirmation message.
    """

    if intent == "play_music":
        vehicle_state["music_status"] = "Playing"
        vehicle_state["music_category"] = "Default"

        return "Playing music."

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