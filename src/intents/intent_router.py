def detect_intent(user_message):
    """
    Detect the user's intended vehicle action.

    Returns:
        A string representing the detected intent.
    """

    message = user_message.lower().strip()

    # -----------------------------
    # Music
    # -----------------------------

    music_phrases = [
        "play music",
        "play a song",
        "play some music",
        "put some music on",
        "put something on",
        "listen to music",
        "start music",
        "play something"
    ]

    if any(phrase in message for phrase in music_phrases):
        return "play_music"

    # -----------------------------
    # Navigation
    # -----------------------------

    navigation_phrases = [
        "take me home",
        "navigate home",
        "navigate to home",
        "route me home",
        "give me directions home",
        "start navigation home",
        "go home"
    ]

    if any(phrase in message for phrase in navigation_phrases):
        return "navigate_home"

    # -----------------------------
    # Temperature
    # -----------------------------

    temperature_keywords = [
        "temperature",
        "degrees",
        "temp",
        "make it warmer",
        "make it colder",
        "cooler",
        "warmer"
    ]

    if any(keyword in message for keyword in temperature_keywords):
        return "set_temperature"

    return "unknown"