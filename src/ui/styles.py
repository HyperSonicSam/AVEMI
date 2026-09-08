from pathlib import Path

import streamlit as st


def apply_styles():
    """Load the AVEMI stylesheet and inject it into the Streamlit app."""
    css_path = Path(__file__).resolve().parents[2] / "assets" / "styles.css"
    css = css_path.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
