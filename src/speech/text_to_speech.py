import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PIPER_MODEL = (
    PROJECT_ROOT
    / "en_GB-jenny_dioco-medium.onnx"
)


def generate_speech(text):
    """
    Generate speech from assistant text using Piper.

    Returns:
        str: Path to the generated WAV file.
    """

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
            str(PIPER_MODEL),
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