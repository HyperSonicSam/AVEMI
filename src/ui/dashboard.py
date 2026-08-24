import streamlit as st

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
        """
<div class="avemi-title">AVEMI</div>
<div class="avemi-subtitle">
Affective Vehicle Emotion-aware Multimodal Intelligence
</div>
""",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Top status bar
    # -----------------------------------------------------

    status_1, status_2, status_3 = st.columns(3)

    with status_1:
        st.markdown(
            """
<div class="avemi-status-card">
<span class="status-online">●</span>
&nbsp; AVEMI Online
</div>
""",
            unsafe_allow_html=True
        )

    with status_2:
        st.markdown(
            """
<div class="avemi-status-card">
<span class="status-blue">◈</span>
&nbsp; Qwen3 4B
</div>
""",
            unsafe_allow_html=True
        )

    with status_3:
        st.markdown(
            """
<div class="avemi-status-card">
<span class="status-blue">🎙</span>
&nbsp; Voice + Text
</div>
""",
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
            f"""
<div class="avemi-card">
<div class="card-label">Cabin Temperature</div>
<div class="card-value blue-value">
{vehicle_state['temperature']}°C
</div>
<div class="card-subtext">
Climate control
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="avemi-card">
<div class="card-label">Fuel Level</div>
<div class="card-value green-value">
{vehicle_state['fuel_level']}%
</div>
<div class="card-subtext">
Vehicle fuel status
</div>
</div>
""",
            unsafe_allow_html=True
        )

        music_category = (
            vehicle_state["music_category"]
        )

        st.markdown(
            f"""
<div class="avemi-card">
<div class="card-label">Media</div>
<div class="card-value purple-value">
{vehicle_state['music_status']}
</div>
<div class="card-subtext">
{music_category}
</div>
</div>
""",
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # Center dashboard - AVEMI HUD
    # -----------------------------------------------------

    with center_dashboard:

        st.markdown(
            """
<div class="hud-wrapper">
<div class="hud-orb">

<div class="hud-ring hud-ring-one"></div>
<div class="hud-ring hud-ring-two"></div>
<div class="hud-ring hud-ring-three"></div>
<div class="hud-ring hud-ring-four"></div>

<div class="hud-core">
<div class="hud-logo">AVEMI</div>

<div class="hud-status">
<span class="hud-dot"></span>
System Active
</div>

</div>
</div>
</div>
""",
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
            f"""
<div class="avemi-card">
<div class="card-label">Navigation</div>
<div class="card-value orange-value">
{navigation_value}
</div>
<div class="card-subtext">
{navigation_detail}
</div>
</div>
""",
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
            f"""
<div class="avemi-card">
<div class="card-label">Driver Emotion</div>
<div class="card-value blue-value">
{displayed_emotion}
</div>
<div class="card-subtext">
{emotion_detail}
</div>
</div>
""",
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # Destination
        # -------------------------------------------------

        destination = (
            vehicle_state["destination"]
        )

        st.markdown(
            f"""
<div class="avemi-card">
<div class="card-label">Destination</div>
<div class="card-value purple-value">
{destination}
</div>
<div class="card-subtext">
Current route target
</div>
</div>
""",
            unsafe_allow_html=True
        )