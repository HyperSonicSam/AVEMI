import streamlit as st

from src.emotion.emotion_manager import (
    get_emotion_context,
    get_emotion_profile
)
from src.intents.intent_router import detect_intent
from src.vehicle.action_manager import (
    execute_action,
    execute_structured_action
) 

from src.llm.ollama_client import generate_response
from src.llm.prompt_builder import build_system_prompt
from src.llm.command_parser import parse_command

st.set_page_config(
    page_title="Emotion-Aware In-Vehicle Assistant",
    page_icon="🚗",
    layout="wide"
)

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


st.title("Emotion-Aware In-Vehicle Assistant")

st.write(
    "Interactive research demonstrator for an "
    "emotion-aware in-vehicle conversational agent."
)

# -----------------------------
# Driver state controls
# -----------------------------

with st.sidebar:
    st.header("Driver State")

    assistant_mode = st.radio(
        "Assistant Mode",
        ["Baseline", "Emotion-Aware"]
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

# -----------------------------
# Emotion context
# -----------------------------

emotion_context = get_emotion_context(
    assistant_mode,
    selected_emotion,
    emotion_confidence
)

emotion_profile = get_emotion_profile(
    emotion_context
)

st.divider()

vehicle_column, conversation_column = st.columns(
    [1, 2],
    gap="large"
)

with vehicle_column:
    st.subheader("Vehicle State")

    vehicle_state = st.session_state.vehicle_state

    st.metric(
        "Temperature",
        f"{vehicle_state['temperature']} °C"
    )

    st.metric(
        "Fuel Level",
        f"{vehicle_state['fuel_level']}%"
    )

    st.write(
        f"**Music:** {vehicle_state['music_status']}"
    )

    st.write(
        f"**Music Category:** {vehicle_state['music_category']}"
    )

    st.write(
        f"**Destination:** {vehicle_state['destination']}"
    )

    if vehicle_state["navigation_active"]:
        st.write("**Navigation:** 🟢 Active")
    else:
        st.write("**Navigation:** ⚪ Inactive")

with conversation_column:
    st.subheader("Conversation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input(
        "Ask the assistant something..."
    )

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
            intent = detect_intent(user_message)

            action_response = execute_action(
                intent,
                user_message,
                st.session_state.vehicle_state,
                emotion_profile
            )

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
                "content": (
                    f"User message: {user_message}\n\n"
                    f"Vehicle action result: {action_response}\n\n"
                )
            }
        ]

        intent = command.get("intent") if command else "unknown"

        # Vehicle actions use deterministic responses.
        # This prevents the LLM from hallucinating or incorrectly
        # describing an action that has already been executed.
        if intent not in ["conversation", "unknown"]:
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

        st.rerun()