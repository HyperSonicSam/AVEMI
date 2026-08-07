def detect_intent(user_message):
    """
    Detect the user's intended vehicle action.

    Returns:
        A string representing the detected intent.
    """

    message = user_message.lower()

    # Music
    if "play" in message and "music" in message:
        return "play_music"

    # Navigation
    if "home" in message and (
        "navigate" in message
        or "take me" in message
        or "route" in message
    ):
        return "navigate_home"

    # Temperature
    if "temperature" in message:
        return "set_temperature"

    return "unknown"