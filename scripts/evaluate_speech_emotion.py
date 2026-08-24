import os
import json
import sys
from pathlib import Path

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score
)


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

METADATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "crema_metadata.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "speech_emotion_cnn.keras"
)

CONFIG_FILE = (
    PROJECT_ROOT
    / "models"
    / "speech_emotion_config.json"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "evaluation"
    / "ser"
)

RESULTS_JSON = (
    RESULTS_DIR
    / "ser_results.json"
)

CONFUSION_MATRIX_FILE = (
    RESULTS_DIR
    / "ser_confusion_matrix.png"
)

CREMA_ROOT = Path(
    os.getenv(
        "CREMA_ROOT",
        PROJECT_ROOT.parent / "datasets" / "CREMA-D"
    )
)

AUDIO_DIR = (
    CREMA_ROOT
    / "AudioWAV"
)


# ---------------------------------------------------------
# Load configuration
# ---------------------------------------------------------

with open(
    CONFIG_FILE,
    "r",
    encoding="utf-8"
) as file:
    CONFIG = json.load(file)


SAMPLE_RATE = CONFIG["sample_rate"]
DURATION = CONFIG["duration"]
N_MELS = CONFIG["n_mels"]
N_FFT = CONFIG["n_fft"]
HOP_LENGTH = CONFIG["hop_length"]

TARGET_SAMPLES = CONFIG["target_samples"]

FEATURE_MEAN = CONFIG["feature_mean"]
FEATURE_STD = CONFIG["feature_std"]

LABELS = CONFIG["labels"]

LABEL_TO_INDEX = {
    label: index
    for index, label in enumerate(LABELS)
}


# ---------------------------------------------------------
# Audio preprocessing
# ---------------------------------------------------------

def load_audio(audio_path):
    audio, _ = librosa.load(
        audio_path,
        sr=SAMPLE_RATE,
        mono=True
    )

    if len(audio) < TARGET_SAMPLES:
        audio = np.pad(
            audio,
            (
                0,
                TARGET_SAMPLES - len(audio)
            )
        )

    elif len(audio) > TARGET_SAMPLES:
        audio = audio[:TARGET_SAMPLES]

    return audio


def create_log_mel(audio):
    mel_spectrogram = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0
    )

    log_mel = librosa.power_to_db(
        mel_spectrogram,
        ref=np.max
    )

    log_mel = (
        log_mel - FEATURE_MEAN
    ) / (FEATURE_STD + 1e-8)

    return log_mel


# ---------------------------------------------------------
# Build test dataset
# ---------------------------------------------------------

def build_test_dataset(df):
    test_df = df[
        df["split"] == "test"
    ].reset_index(drop=True)

    features = []
    labels = []

    total = len(test_df)

    print(
        f"\nProcessing test split: "
        f"{total} samples"
    )

    for index, row in test_df.iterrows():

        audio_path = (
            AUDIO_DIR
            / row["audio_path"]
        )

        audio = load_audio(
            audio_path
        )

        log_mel = create_log_mel(
            audio
        )

        features.append(
            log_mel
        )

        labels.append(
            LABEL_TO_INDEX[
                row["emotion"]
            ]
        )

        if (
            (index + 1) % 100 == 0
            or index + 1 == total
        ):
            print(
                f"  {index + 1}/{total}"
            )

    X_test = np.array(
        features,
        dtype=np.float32
    )

    y_test = np.array(
        labels,
        dtype=np.int64
    )

    X_test = X_test[
        ...,
        np.newaxis
    ]

    return X_test, y_test


# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

def evaluate():
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found:\n"
            f"{METADATA_FILE}"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model file not found:\n"
            f"{MODEL_FILE}"
        )

    print(
        "\nAVEMI SPEECH EMOTION EVALUATION"
    )

    print(
        "=" * 60
    )

    df = pd.read_csv(
        METADATA_FILE
    )

    X_test, y_test = (
        build_test_dataset(
            df
        )
    )

    print(
        f"\nTest input shape: "
        f"{X_test.shape}"
    )

    print(
        "\nLoading trained model..."
    )

    model = tf.keras.models.load_model(
        MODEL_FILE
    )

    print(
        "Running predictions..."
    )

    probabilities = model.predict(
        X_test,
        verbose=1
    )

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro"
    )

    weighted_f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    report = classification_report(
        y_test,
        predictions,
        target_names=LABELS,
        digits=4,
        output_dict=True
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    # -----------------------------------------------------
    # Terminal results
    # -----------------------------------------------------

    print(
        f"\nTest accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro F1: "
        f"{macro_f1:.4f}"
    )

    print(
        f"Weighted F1: "
        f"{weighted_f1:.4f}"
    )

    print(
        "\nClassification report:\n"
    )

    print(
        classification_report(
            y_test,
            predictions,
            target_names=LABELS,
            digits=4
        )
    )

    print(
        "\nConfusion matrix:\n"
    )

    print(
        matrix
    )

    # -----------------------------------------------------
    # Save result files
    # -----------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results = {
        "test_samples":
            int(len(y_test)),

        "accuracy":
            float(accuracy),

        "macro_f1":
            float(macro_f1),

        "weighted_f1":
            float(weighted_f1),

        "labels":
            LABELS,

        "classification_report":
            report,

        "confusion_matrix":
            matrix.tolist()
    }

    with open(
        RESULTS_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2
        )

    # -----------------------------------------------------
    # Confusion matrix figure
    # -----------------------------------------------------

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=LABELS
    )

    fig, ax = plt.subplots(
        figsize=(9, 8)
    )

    display.plot(
        ax=ax,
        values_format="d"
    )

    ax.set_title(
        "AVEMI Speech Emotion Recognition"
    )

    fig.tight_layout()

    fig.savefig(
        CONFUSION_MATRIX_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(
        f"\nResults saved to:\n"
        f"{RESULTS_JSON}"
    )

    print(
        f"\nConfusion matrix saved to:\n"
        f"{CONFUSION_MATRIX_FILE}"
    )


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    evaluate()