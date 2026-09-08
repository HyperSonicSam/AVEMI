from pathlib import Path
import os
import random

import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CREMA_ROOT = Path(
    os.getenv(
        "CREMA_ROOT",
        PROJECT_ROOT.parent / "datasets" / "CREMA-D"
    )
)

AUDIO_DIR = CREMA_ROOT / "AudioWAV"

OUTPUT_FILE = PROJECT_ROOT / "data" / "crema_metadata.csv"

RANDOM_SEED = 42


EMOTION_MAP = {
    "ANG": "angry",
    "DIS": "disgust",
    "FEA": "fear",
    "HAP": "happy",
    "NEU": "neutral",
    "SAD": "sad",
}


INTENSITY_MAP = {
    "LO": "low",
    "MD": "medium",
    "HI": "high",
    "XX": "unspecified",
}


# ---------------------------------------------------------
# Read CREMA-D filenames
# ---------------------------------------------------------

def build_metadata():
    rows = []

    wav_files = sorted(AUDIO_DIR.glob("*.wav"))

    for audio_path in wav_files:
        parts = audio_path.stem.split("_")

        if len(parts) != 4:
            print(f"Skipping unexpected filename: {audio_path.name}")
            continue

        actor_id, sentence_code, emotion_code, intensity_code = parts

        if emotion_code not in EMOTION_MAP:
            print(f"Skipping unknown emotion: {audio_path.name}")
            continue

        rows.append(
            {
                "filename": audio_path.name,
                "actor_id": int(actor_id),
                "sentence_code": sentence_code,
                "emotion_code": emotion_code,
                "emotion": EMOTION_MAP[emotion_code],
                "intensity_code": intensity_code,
                "intensity": INTENSITY_MAP.get(
                    intensity_code,
                    "unknown"
                ),
                "audio_path": audio_path.name,
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------
# Create speaker-independent splits
# ---------------------------------------------------------

def assign_splits(df):
    actors = sorted(df["actor_id"].unique())

    random.seed(RANDOM_SEED)
    random.shuffle(actors)

    total_actors = len(actors)

    train_count = round(total_actors * 0.80)
    validation_count = round(total_actors * 0.10)

    train_actors = set(
        actors[:train_count]
    )

    validation_actors = set(
        actors[
            train_count:
            train_count + validation_count
        ]
    )

    test_actors = set(
        actors[
            train_count + validation_count:
        ]
    )

    def get_split(actor_id):
        if actor_id in train_actors:
            return "train"

        if actor_id in validation_actors:
            return "validation"

        return "test"

    df["split"] = df["actor_id"].apply(get_split)

    return df


# ---------------------------------------------------------
# Dataset summary
# ---------------------------------------------------------

def print_summary(df):
    print("\nCREMA-D DATASET SUMMARY")
    print("=" * 50)

    print(f"\nTotal samples: {len(df)}")
    print(f"Total actors: {df['actor_id'].nunique()}")

    print("\nEmotion distribution:")
    print(
        df["emotion"]
        .value_counts()
        .sort_index()
    )

    print("\nActor distribution:")
    print(
        df.groupby("split")["actor_id"]
        .nunique()
    )

    print("\nSample distribution:")
    print(
        df["split"]
        .value_counts()
    )

    print("\nEmotion distribution by split:")
    print(
        pd.crosstab(
            df["split"],
            df["emotion"]
        )
    )

    print("\nChecking actor leakage...")

    train_actors = set(
        df[df["split"] == "train"]["actor_id"]
    )

    validation_actors = set(
        df[df["split"] == "validation"]["actor_id"]
    )

    test_actors = set(
        df[df["split"] == "test"]["actor_id"]
    )

    leakage = (
        train_actors & validation_actors
        or train_actors & test_actors
        or validation_actors & test_actors
    )

    if leakage:
        print("WARNING: Actor leakage detected!")
    else:
        print("No actor leakage detected.")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    if not AUDIO_DIR.exists():
        raise FileNotFoundError(
            "CREMA-D AudioWAV directory not found:\n"
            f"{AUDIO_DIR}\n\n"
            "Set the CREMA_ROOT environment variable to your local CREMA-D "
            "directory and run the script again."
        )

    print("Reading CREMA-D...")

    df = build_metadata()

    df = assign_splits(df)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print_summary(df)

    print(
        f"\nMetadata saved to: "
        f"{OUTPUT_FILE.resolve()}"
    )


if __name__ == "__main__":
    main()
