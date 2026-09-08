from html import escape
from pathlib import Path

import streamlit as st


TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def _load_template(name):
    """Load a reusable HTML fragment for the dashboard."""
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def _render_template(name, **values):
    """Render a dashboard HTML fragment with escaped dynamic values."""
    template = _load_template(name)
    safe_values = {
        key: escape(str(value))
        for key, value in values.items()
    }
    return template.format(**safe_values)


def render_dashboard(
    vehicle_state,
    assistant_mode
):
    """
    Render the main AVEMI dashboard.
    """

    # -----------------------------------------------------
    # AVEMI heading
    # -----------------------------------------------------

    st.markdown(
        _load_template("header.html"),
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Top status bar
    # -----------------------------------------------------

    status_1, status_2, status_3 = st.columns(3)

    with status_1:
        st.markdown(
            _render_template(
                "status_card.html",
                status_class="status-online",
                icon="●",
                label="AVEMI Online"
            ),
            unsafe_allow_html=True
        )

    with status_2:
        st.markdown(
            _render_template(
                "status_card.html",
                status_class="status-blue",
                icon="◈",
                label="Qwen3 4B"
            ),
            unsafe_allow_html=True
        )

    with status_3:
        st.markdown(
            _render_template(
                "status_card.html",
                status_class="status-blue",
                icon="🎙",
                label="Voice + Text"
            ),
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # Dashboard layout
    # -----------------------------------------------------

    left_dashboard, center_dashboard, right_dashboard = (
        st.columns(
            [0.9, 1.65, 1.1],
            gap="large"
        )
    )

    # -----------------------------------------------------
    # Left dashboard - Vehicle
    # -----------------------------------------------------

    with left_dashboard:

        st.markdown("#### 🚘 Vehicle")

        st.markdown(
            _render_template(
                "card.html",
                label="Cabin Temperature",
                value_class="blue-value",
                value=f"{vehicle_state['temperature']}°C",
                subtext="Climate control"
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            _render_template(
                "card.html",
                label="Fuel Level",
                value_class="green-value",
                value=f"{vehicle_state['fuel_level']}%",
                subtext="Vehicle fuel status"
            ),
            unsafe_allow_html=True
        )

        music_category = (
            vehicle_state["music_category"]
        )

        st.markdown(
            _render_template(
                "card.html",
                label="Media",
                value_class="purple-value",
                value=vehicle_state["music_status"],
                subtext=music_category
            ),
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # Center dashboard - AVEMI HUD
    # -----------------------------------------------------

    with center_dashboard:

        st.markdown(
            _load_template("hud.html"),
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # Right dashboard - Journey
    # -----------------------------------------------------

    with right_dashboard:

        st.markdown("#### Journey")

        # -------------------------------------------------
        # Navigation
        # -------------------------------------------------

        if vehicle_state["navigation_active"]:
            navigation_value = "Active"
            navigation_detail = (
                vehicle_state["destination"]
            )

        else:
            navigation_value = "Inactive"
            navigation_detail = "No active route"

        st.markdown(
            _render_template(
                "card.html",
                label="Navigation",
                value_class="orange-value",
                value=navigation_value,
                subtext=navigation_detail
            ),
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # Driver emotion
        # -------------------------------------------------

        if assistant_mode == "Emotion-Aware":

            detected_emotion = (
                st.session_state.detected_emotion
            )

            detected_confidence = (
                st.session_state
                .detected_emotion_confidence
            )

            if detected_confidence >= 0.45:

                displayed_emotion = (
                    detected_emotion.capitalize()
                )

                emotion_detail = (
                    f"Confidence: "
                    f"{detected_confidence * 100:.1f}%"
                )

            else:

                displayed_emotion = "Uncertain"

                emotion_detail = (
                    f"Confidence: "
                    f"{detected_confidence * 100:.1f}%"
                )

        else:

            displayed_emotion = "Disabled"
            emotion_detail = "Baseline mode"

        st.markdown(
            _render_template(
                "card.html",
                label="Driver Emotion",
                value_class="blue-value",
                value=displayed_emotion,
                subtext=emotion_detail
            ),
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # Destination
        # -------------------------------------------------

        destination = (
            vehicle_state["destination"]
        )

        st.markdown(
            _render_template(
                "card.html",
                label="Destination",
                value_class="purple-value",
                value=destination,
                subtext="Current route target"
            ),
            unsafe_allow_html=True
        )
