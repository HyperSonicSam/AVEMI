import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VOICE_NAME = "en_GB-jenny_dioco-medium.onnx"


def _resolve_piper_model() -> Path:
    """Resolve the Piper voice model from supported local locations."""

    configured_path = os.getenv("PIPER_MODEL_PATH")
    if configured_path:
        configured_model = Path(configured_path).expanduser().resolve()
        if configured_model.exists():
            return configured_model

    managed_model = (
        PROJECT_ROOT
        / "models"
        / "piper"
        / VOICE_NAME
    )
    if managed_model.exists():
        return managed_model

    # Backwards-compatible fallback for older local AVEMI setups.
    legacy_model = PROJECT_ROOT / VOICE_NAME
    if legacy_model.exists():
        return legacy_model

    raise RuntimeError(
        "Piper voice model is not installed.\n\n"
        "Run:\n"
        "    python scripts/setup_piper_voice.py\n\n"
        "or set PIPER_MODEL_PATH to the full path of a compatible "
        "Piper .onnx voice model."
    )


def generate_speech(text):
    """
    Generate speech from assistant text using Piper.

    Returns:
        str: Path to the generated WAV file.
    """

    piper_model = _resolve_piper_model()

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    temp_path = temp_file.name
    temp_file.close()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "piper",
            "-m",
            str(piper_model),
            "-f",
            temp_path
        ],
        input=text,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Piper failed to generate speech.\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    return temp_path
