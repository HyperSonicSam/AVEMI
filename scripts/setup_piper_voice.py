"""Download the Piper voice used by AVEMI.

The voice files are runtime assets and are intentionally excluded from Git.
Run this script after installing requirements.txt.
"""

from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VOICE_DIR = PROJECT_ROOT / "models" / "piper"

VOICE_NAME = "en_GB-jenny_dioco-medium"
BASE_URL = (
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
    "en/en_GB/jenny_dioco/medium"
)

FILES = {
    f"{VOICE_NAME}.onnx": {
        "url": f"{BASE_URL}/{VOICE_NAME}.onnx?download=true",
        "md5": "d08f2f7edf0c858275a7eca74ff2a9e4",
    },
    f"{VOICE_NAME}.onnx.json": {
        "url": f"{BASE_URL}/{VOICE_NAME}.onnx.json?download=true",
        "md5": "5338cad16dcd408d2b0a247cf163abac",
    },
}


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".part")
    try:
        print(f"Downloading {destination.name}...")
        urllib.request.urlretrieve(url, temporary)
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    VOICE_DIR.mkdir(parents=True, exist_ok=True)

    for filename, metadata in FILES.items():
        destination = VOICE_DIR / filename
        expected_md5 = metadata["md5"]

        if destination.exists() and md5sum(destination) == expected_md5:
            print(f"Already present: {destination}")
            continue

        download_file(metadata["url"], destination)

        actual_md5 = md5sum(destination)
        if actual_md5 != expected_md5:
            destination.unlink(missing_ok=True)
            raise RuntimeError(
                f"Checksum verification failed for {filename}. "
                f"Expected {expected_md5}, got {actual_md5}."
            )

        print(f"Verified: {destination}")

    print("\nPiper voice setup complete.")
    print(f"Voice directory: {VOICE_DIR}")


if __name__ == "__main__":
    main()
