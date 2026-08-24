import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        /* Main application */
        .stApp {
            background:
                radial-gradient(
                    circle at 75% 10%,
                    rgba(45, 100, 160, 0.12),
                    transparent 30%
                ),
                #0b0f14;
        }

        /* Main content */
        .block-container {
            padding-top: 3.2rem;
            padding-bottom: 0.5rem;
            max-width: 1500px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #10161d;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 16px;
            border-radius: 14px;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 6px 10px;
            margin-bottom: 8px;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        /* Reduce visual clutter */
        hr {
            border-color: rgba(255, 255, 255, 0.08);
        }

        /* AVEMI heading */
        .avemi-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0;
        }

        .avemi-subtitle {
            opacity: 0.65,
            font-size: 0.82rem;
            margin-top: -12px;
            margin-bottom: 12px;
        }

        .status-label {
            opacity: 0.65;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        /* -------------------------------------------------
        AVEMI central HUD
        -------------------------------------------------- */

        .hud-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 390px;
            min-height: 400px;
            width: 100%;
            position: relative;

            /* Fine-tune HUD position */
            transform: translate(18px, 25px);
        }

        .hud-orb {
            width: 410px;
            height: 410px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .hud-ring {
            position: absolute;
            border-radius: 50%;
            border-style: solid;
            border-color: rgba(40, 190, 255, 0.7);
            box-shadow:
                0 0 18px rgba(0, 174, 255, 0.25),
                inset 0 0 18px rgba(0, 174, 255, 0.08);
        }

        .hud-ring-one {
            width: 390px;
            height: 390px;
            border-width: 2px;
            border-top-color: #24c8ff;
            border-right-color: rgba(36, 200, 255, 0.15);
            animation: rotateClockwise 12s linear infinite;
        }

        .hud-ring-two {
            width: 335px;
            height: 335px;
            border-width: 5px;
            border-left-color: #3887ff;
            border-bottom-color: rgba(56, 135, 255, 0.15);
            animation: rotateCounterClockwise 8s linear infinite;
        }

        .hud-ring-three {
            width: 280px;
            height: 280px;
            border-width: 2px;
            border-top-color: #5de7ff;
            border-bottom-color: rgba(93, 231, 255, 0.1);
            animation: rotateClockwise 5s linear infinite;
        }

        .hud-ring-four {
            width: 220px;
            height: 220px;
            border-width: 1px;
            border-color: rgba(75, 185, 255, 0.35);
            animation: pulseHUD 2.5s ease-in-out infinite;
        }

        .hud-core {
            position: absolute;
            width: 170px;
            height: 170px;
            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(30, 155, 255, 0.22),
                    rgba(4, 17, 29, 0.9) 65%
                );

            border: 1px solid rgba(70, 190, 255, 0.45);

            box-shadow:
                0 0 35px rgba(0, 170, 255, 0.22),
                inset 0 0 30px rgba(0, 170, 255, 0.15);

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            z-index: 5;
        }

        .hud-logo {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 0.12em;
        }

        .hud-status {
            margin-top: 5px;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.13em;
            color: #55d8ff;
        }

        .hud-dot {
            width: 6px;
            height: 6px;
            background: #5effb5;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
            box-shadow: 0 0 8px #5effb5;
        }

        @keyframes rotateClockwise {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        @keyframes rotateCounterClockwise {
            from {
                transform: rotate(360deg);
            }

            to {
                transform: rotate(0deg);
            }
        }

        @keyframes pulseHUD {
            0%, 100% {
                transform: scale(1);
                opacity: 0.65;
            }

            50% {
                transform: scale(1.06);
                opacity: 1;
            }
        }


        /* -------------------------------------------------
        Dashboard cards
        -------------------------------------------------- */

        .avemi-card {
            background:
                linear-gradient(
                    135deg,
                    rgba(17, 29, 41, 0.88),
                    rgba(9, 16, 24, 0.82)
                );

            border: 1px solid rgba(75, 170, 230, 0.20);
            border-radius: 15px;

            padding: 15px 18px;
            margin-bottom: 12px;

            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.20),
                inset 0 0 25px rgba(0, 130, 220, 0.025);
        }

        .card-label {
            color: #8294a6;
            font-size: 0.70rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .card-value {
            font-size: 1.35rem;
            font-weight: 600;
            margin-top: 4px;
        }

        .card-subtext {
            color: #748597;
            font-size: 0.76rem;
            margin-top: 3px;
        }

        .blue-value {
            color: #55d8ff;
        }

        .green-value {
            color: #63e6a5;
        }

        .purple-value {
            color: #b98cff;
        }

        .orange-value {
            color: #ffad66;
        }

        /* Compact Streamlit headings */
        h1, h2, h3, h4 {
            margin-top: 0.25rem !important;
            margin-bottom: 0.35rem !important;
        }

        /* Compact chat messages */
        [data-testid="stChatMessage"] {
            padding: 3px 8px;
            margin-bottom: 4px;
        }

        /* Hide footer */
        footer {
            visibility: hidden;
        }

        /* Compact microphone recorder */
        [data-testid="stAudioInput"] {
            margin-top: -4px;
        }

        [data-testid="stAudioInput"] > div {
            min-height: 48px !important;
        }

        /* Tighten vertical spacing between Streamlit blocks */
        [data-testid="stVerticalBlock"] {
            gap: 0.45rem;
        }

        /* Streamlit top toolbar */
        [data-testid="stToolbar"] {
            opacity: 0.35;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        /* AVEMI input field */
        [data-testid="stTextInput"] input {
            height: 52px;
            border-radius: 12px;
            background: rgba(30, 34, 45, 0.95);
            border: 1px solid rgba(80, 160, 220, 0.15);
        }

        /* Input action buttons */
        .stButton > button {
            min-height: 52px;
            border-radius: 12px;
            font-size: 1.15rem;
        }

        /* Popover microphone button */
        [data-testid="stPopover"] button {
            min-height: 52px;
            border-radius: 12px;
        }

        /* -------------------------------------------------
        AVEMI message input
        -------------------------------------------------- */

        [data-testid="stTextInput"] input {
            height: 52px;
            border-radius: 13px;
            padding-left: 16px;

            background:
                linear-gradient(
                    135deg,
                    rgba(31, 36, 48, 0.98),
                    rgba(24, 29, 39, 0.98)
                );

            border: 1px solid rgba(70, 170, 230, 0.16);

            color: #f2f7fb;

            box-shadow:
                inset 0 0 18px rgba(0, 125, 210, 0.025);
        }

        [data-testid="stTextInput"] input:focus {
            border-color: rgba(55, 195, 255, 0.65);

            box-shadow:
                0 0 0 1px rgba(55, 195, 255, 0.18),
                0 0 18px rgba(0, 160, 230, 0.08);

            outline: none;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: rgba(210, 222, 232, 0.55);
        }

        /* -------------------------------------------------
        AVEMI action buttons
        -------------------------------------------------- */

        [data-testid="stPopover"] > button,
        .stButton > button {
            min-height: 52px;
            border-radius: 13px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20, 31, 43, 0.98),
                    rgba(12, 22, 32, 0.98)
                );

            border: 1px solid rgba(48, 185, 245, 0.28);

            color: #dff6ff;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                transform 0.15s ease;
        }

        [data-testid="stPopover"] > button:hover,
        .stButton > button:hover {
            border-color: rgba(65, 205, 255, 0.75);

            box-shadow:
                0 0 16px rgba(0, 175, 255, 0.16);

            transform: translateY(-1px);
        }

        [data-testid="stPopover"] > button:active,
        .stButton > button:active {
            transform: translateY(0);
        }

        /* -------------------------------------------------
        Top status bar
        -------------------------------------------------- */

        .avemi-status-card {
            background: rgba(12, 22, 31, 0.58);

            border: 1px solid rgba(72, 159, 213, 0.13);

            border-radius: 10px;

            padding: 7px 12px;

            font-size: 0.82rem;

            color: rgba(238, 246, 252, 0.92);
        }

        .status-online {
            color: #69f0b4;
        }

        .status-blue {
            color: #61d8ff;
        }

        /* -------------------------------------------------
        AVEMI microphone recorder button
        -------------------------------------------------- */

        /* Mic recorder wrapper */
        div:has(> iframe[title*="streamlit_mic_recorder"]) {
            width: 100% !important;
        }

        /* Mic recorder component */
        iframe[title*="streamlit_mic_recorder"] {
            width: 100% !important;
            min-width: 100% !important;
            height: 54px !important;

            border: none !important;
            outline: none !important;

            border-radius: 13px !important;

            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )