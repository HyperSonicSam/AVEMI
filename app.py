import streamlit as st

from src.ui.styles import apply_styles
from src.ui.dashboard import render_dashboard
from src.ui.sidebar import render_sidebar

from src.emotion.emotion_manager import (
    get_emotion_context,
    get_emotion_profile
)
from src.intents.intent_router import detect_intent
from src.vehicle.action_manager import (
    execute_action,
    execute_structured_action
) 

from src.emotion.speech_emotion_recognizer import predict_emotion

from src.llm.ollama_client import generate_response
from src.llm.prompt_builder import build_system_prompt
from src.llm.command_parser import parse_command

from streamlit_mic_recorder import mic_recorder

from src.speech.speech_to_text import transcribe_audio
from src.speech.text_to_speech import generate_speech

st.set_page_config(
    page_title="AVEMI",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()

# -----------------------------
# Vehicle state
# -----------------------------

if "vehicle_state" not in st.session_state:
    st.session_state.vehicle_state = {
        "temperature": 22,
        "music_status": "Paused",
        "music_category": "None",
        "destination": "None",
        "navigation_active": False,
        "fuel_level": 62
    }

# -----------------------------
# Conversation state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. I am your in-vehicle assistant. "
                "How can I help with your journey?"
            )
        }
    ]

# -----------------------------
# Voice state
# -----------------------------

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

if "last_response_audio" not in st.session_state:
    st.session_state.last_response_audio = None

if "voice_input_version" not in st.session_state:
    st.session_state.voice_input_version = 0

# -----------------------------
# Speech emotion state
# -----------------------------

if "detected_emotion" not in st.session_state:
    st.session_state.detected_emotion = "neutral"

if "detected_emotion_confidence" not in st.session_state:
    st.session_state.detected_emotion_confidence = 0.0

(
    assistant_mode,
    selected_emotion,
    emotion_confidence,
    voice_responses
) = render_sidebar()

# -----------------------------
# Emotion context
# -----------------------------

if assistant_mode == "Emotion-Aware":

    detected_emotion = (
        st.session_state.detected_emotion
    )

    detected_confidence = (
        st.session_state.detected_emotion_confidence
    )

    # Use automatic speech emotion recognition
    # only when the prediction is sufficiently confident.
    if detected_confidence >= 0.45:

        active_emotion = (
            detected_emotion.capitalize()
        )

        active_confidence = int(
            detected_confidence * 100
        )

    else:

        # Safe fallback for uncertain predictions.
        active_emotion = "Neutral"
        active_confidence = int(
            detected_confidence * 100
        )

else:

    active_emotion = "Neutral"
    active_confidence = 0


emotion_context = get_emotion_context(
    assistant_mode,
    active_emotion,
    active_confidence
)

emotion_profile = get_emotion_profile(
    emotion_context
)

voice_message = None

vehicle_state = (
    st.session_state.vehicle_state
)

render_dashboard(
    vehicle_state,
    assistant_mode
)

# -----------------------------
# AVEMI conversation bar
# -----------------------------

st.markdown("#### AVEMI Assistant")

chat_container = st.container(
    height=95,
    border=True
)

with chat_container:
    for message in st.session_state.messages[-4:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# -----------------------------
# AVEMI voice output
# -----------------------------

if (
    voice_responses
    and st.session_state.last_response_audio
):
    st.audio(
        st.session_state.last_response_audio,
        format="audio/wav",
        autoplay=True
    )

# -----------------------------
# Text input
# -----------------------------

# -----------------------------
# Text + Voice input
# -----------------------------

text_form_column, mic_column = st.columns(
    [10.5, 1.2],
    gap="small"
)

with text_form_column:
    with st.form(
        "avemi_message_form",
        clear_on_submit=True,
        enter_to_submit=True,
        border=False
    ):
        text_column, send_column = st.columns(
            [10, 1],
            gap="small"
        )

        with text_column:
            typed_message = st.text_input(
                "Message AVEMI",
                placeholder="Message AVEMI...",
                label_visibility="collapsed"
            )

        with send_column:
            send_message = st.form_submit_button(
                "➜",
                use_container_width=True
            )

with mic_column:
    audio = mic_recorder(
        start_prompt="🎙️",
        stop_prompt="⏹",
        just_once=True,
        use_container_width=True,
        key="avemi_mic"
    )


voice_message = None

if audio:
    with st.spinner("Listening..."):

        # ---------------------------------
        # 1. Convert speech to text
        # ---------------------------------

        voice_message = transcribe_audio(
            audio["bytes"]
        )

        # ---------------------------------
        # 2. Create temporary audio files
        # ---------------------------------

        import tempfile
        import os
        import subprocess

        input_path = None
        wav_path = None

        try:
            # Save the raw microphone recording.
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".webm"
            ) as temp_input:

                temp_input.write(
                    audio["bytes"]
                )

                input_path = temp_input.name

            # Create an output path for a proper WAV file.
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ) as temp_wav:

                wav_path = temp_wav.name

            # ---------------------------------
            # 3. Convert to 16 kHz mono WAV
            # ---------------------------------

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_path,
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    wav_path
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

            # ---------------------------------
            # 4. Detect emotion
            # ---------------------------------

            emotion_result = predict_emotion(
                wav_path
            )

            st.session_state.detected_emotion = (
                emotion_result["emotion"]
            )

            st.session_state.detected_emotion_confidence = (
                emotion_result["confidence"]
            )

        finally:

            # ---------------------------------
            # 5. Delete temporary files
            # ---------------------------------

            if (
                input_path
                and os.path.exists(input_path)
            ):
                os.remove(input_path)

            if (
                wav_path
                and os.path.exists(wav_path)
            ):
                os.remove(wav_path)

# -----------------------------
# Process user message
# -----------------------------

user_message = None

if voice_message:
    user_message = voice_message

elif send_message and typed_message.strip():
    user_message = typed_message.strip()

if user_message:

    command = parse_command(
        user_message,
        st.session_state.vehicle_state,
        st.session_state.messages
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    if command:
        action_response = execute_structured_action(
            command,
            st.session_state.vehicle_state,
            emotion_profile
        )

    else:
        intent = detect_intent(
            user_message
        )

        action_response = execute_action(
            intent,
            user_message,
            st.session_state.vehicle_state,
            emotion_profile
        )

    intent = (
        command.get("intent")
        if command
        else "unknown"
    )

    # Vehicle actions use deterministic responses.
    if intent not in [
        "conversation",
        "unknown"
    ]:
        assistant_response = action_response

    else:
        system_prompt = build_system_prompt(
            emotion_context,
            emotion_profile,
            st.session_state.vehicle_state
        )

        llm_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        assistant_response = generate_response(
            llm_messages
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    if voice_responses:
        audio_path = generate_speech(
            assistant_response
        )

        st.session_state.last_response_audio = (
            audio_path
        )

    st.rerun()