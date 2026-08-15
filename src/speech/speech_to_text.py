import tempfile

from faster_whisper import WhisperModel


MODEL_SIZE = "small"

whisper_model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_file):
    """
    Convert recorded audio into text using faster-whisper.

    Args:
        audio_file: Streamlit UploadedFile returned by st.audio_input()

    Returns:
        str: Transcribed text.
    """

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_file:
        if isinstance(audio_file, bytes):
            audio_bytes = audio_file
        else:
            audio_bytes = audio_file.getvalue()

        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    segments, _ = whisper_model.transcribe(
        temp_path,
        language="en"
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return text.strip()