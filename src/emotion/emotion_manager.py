import json
from pathlib import Path


def get_emotion_context(
    assistant_mode,
    selected_emotion,
    emotion_confidence
):
    """
    Create the emotional context used by the assistant.

    In Baseline mode, emotional information is ignored.
    In Emotion-Aware mode, the simulated emotion is used.
    """

    if assistant_mode == "Baseline":
        return {
            "enabled": False,
            "emotion": None,
            "confidence": None
        }

    return {
        "enabled": True,
        "emotion": selected_emotion.lower(),
        "confidence": emotion_confidence
    }


def get_emotion_profile(emotion_context):
    """
    Load the behavioural profile for the current emotion.

    Returns None when emotion awareness is disabled.
    """

    if not emotion_context["enabled"]:
        return None

    file_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "emotion_profiles.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        profiles = json.load(file)

    emotion = emotion_context["emotion"]

    return profiles.get(emotion)