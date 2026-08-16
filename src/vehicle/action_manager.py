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
            music_category = emotion_profile.get(
                "music_category",
                "default"
            )
        else:
            music_category = "default"

        vehicle_state["music_category"] = music_category.capitalize()

        return (
            f"Playing "
            f"{vehicle_state['music_category'].lower()} music."
        )

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

    if intent == "cancel_navigation":

        if vehicle_state["navigation_active"]:
            vehicle_state["navigation_active"] = False
            vehicle_state["destination"] = "None"

            return "Navigation cancelled."

        return "Navigation is not currently active."

    if intent == "pause_music":

        if vehicle_state["music_status"] == "Playing":
            vehicle_state["music_status"] = "Paused"

            return "Music paused."

        return "Music is already paused."

    if intent == "resume_music":

        if vehicle_state["music_status"] == "Playing":
            return "Music is already playing."

        if vehicle_state["music_category"] == "None":
            return "There is no paused music to resume."

        vehicle_state["music_status"] = "Playing"

        return (
            f"Resuming "
            f"{vehicle_state['music_category'].lower()} music."
        )

    if intent == "navigate_to":
        destination = command.get("destination")

        if not destination:
            return "I need a destination to start navigation."

        vehicle_state["destination"] = destination
        vehicle_state["navigation_active"] = True

        return f"Starting navigation to {destination}."

    if intent == "get_fuel_level":
        return (
            f"Your current fuel level is "
            f"{vehicle_state['fuel_level']}%."
        )


    if intent == "get_temperature":
        return (
            f"The cabin temperature is "
            f"{vehicle_state['temperature']}°C."
        )


    if intent == "get_music_status":
        music_status = vehicle_state["music_status"]
        music_category = vehicle_state["music_category"]

        if music_status.lower() == "playing":
            return (
                f"Music is currently playing. "
                f"The category is {music_category.lower()}."
            )

        return (
            f"Music is currently "
            f"{music_status.lower()}."
        )


    if intent == "get_navigation_status":
        if vehicle_state["navigation_active"]:
            return (
                f"Navigation is currently active to "
                f"{vehicle_state['destination']}."
            )

        return "Navigation is currently inactive."


    if intent == "get_destination":
        destination = vehicle_state["destination"]

        if (
            destination == "None"
            or not vehicle_state["navigation_active"]
        ):
            return (
                "There is currently no active destination."
            )

        return (
            f"The current destination is "
            f"{destination}."
        )

    return "I couldn't identify a vehicle action."