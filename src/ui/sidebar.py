import streamlit as st


def render_sidebar():
    """
    Render the AVEMI sidebar controls.

    Returns:
        tuple:
            assistant_mode,
            selected_emotion,
            emotion_confidence,
            voice_responses
    """

    with st.sidebar:
        st.header("AVEMI Controls")

        assistant_mode = st.radio(
            "Assistant Mode",
            [
                "Baseline",
                "Emotion-Aware"
            ]
        )

        selected_emotion = st.selectbox(
            "Simulated Emotion",
            [
                "Neutral",
                "Happy",
                "Sad",
                "Angry",
                "Stressed",
                "Tired"
            ]
        )

        emotion_confidence = st.slider(
            "Emotion Confidence",
            min_value=0,
            max_value=100,
            value=85
        )

        st.divider()

        st.subheader("Voice")

        voice_responses = st.toggle(
            "Voice Responses",
            value=True
        )

    return (
        assistant_mode,
        selected_emotion,
        emotion_confidence,
        voice_responses
    )