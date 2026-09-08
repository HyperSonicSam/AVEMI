from pathlib import Path

import os
import librosa
import numpy as np
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score
)

import tensorflow as tf
from tensorflow.keras import layers, models


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

METADATA_FILE = PROJECT_ROOT / "data" / "crema_metadata.csv"

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

SAMPLE_RATE = 16000
DURATION = 5.0

N_MELS = 64
N_FFT = 1024
HOP_LENGTH = 256

TARGET_SAMPLES = int(
    SAMPLE_RATE * DURATION
)

MODEL_OUTPUT = PROJECT_ROOT / "models" / "speech_emotion_cnn.keras"

LABELS = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "neutral",
    "sad"
]

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
    else:
        audio = audio[:TARGET_SAMPLES]

    return audio


def extract_features(audio):
    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0
    )

    log_mel = librosa.power_to_db(
        mel,
        ref=np.max
    )

    return log_mel.astype(np.float32)


def load_split(df, split_name):
    split_df = df[df["split"] == split_name]

    features = []
    labels = []

    for _, row in split_df.iterrows():
        audio_path = AUDIO_DIR / row["audio_path"]

        audio = load_audio(audio_path)
        feature = extract_features(audio)

        features.append(feature)
        labels.append(
            LABEL_TO_INDEX[row["emotion"]]
        )

    X = np.array(features)[..., np.newaxis]
    y = np.array(labels)

    return X, y


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------

def build_model(input_shape):
    model = models.Sequential([
        layers.Input(shape=input_shape),

        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.35),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.25),
        layers.Dense(len(LABELS), activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}\n"
            "Run scripts/prepare_crema.py first."
        )

    if not AUDIO_DIR.exists():
        raise FileNotFoundError(
            "CREMA-D AudioWAV directory not found:\n"
            f"{AUDIO_DIR}\n\n"
            "Set the CREMA_ROOT environment variable to your local CREMA-D "
            "directory and run the script again."
        )

    df = pd.read_csv(METADATA_FILE)

    print("Loading training split...")
    X_train, y_train = load_split(df, "train")

    print("Loading validation split...")
    X_val, y_val = load_split(df, "validation")

    print("Loading test split...")
    X_test, y_test = load_split(df, "test")

    model = build_model(X_train.shape[1:])

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6
        )
    ]

    model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=40,
        batch_size=32,
        callbacks=callbacks
    )

    probabilities = model.predict(
        X_test,
        verbose=0
    )

    predictions = np.argmax(
        probabilities,
        axis=1
    )

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

    print("\nTest accuracy:", accuracy)
    print("Macro F1:", macro_f1)
    print("Weighted F1:", weighted_f1)

    print("\nClassification report:\n")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=LABELS,
            digits=4
        )
    )

    print("\nConfusion matrix:\n")
    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    MODEL_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    model.save(MODEL_OUTPUT)

    print(f"\nModel saved to: {MODEL_OUTPUT}")


if __name__ == "__main__":
    main()
