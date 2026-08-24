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

METADATA_FILE = Path("data") / "crema_metadata.csv"

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

MODEL_OUTPUT = Path("models") / "speech_emotion_cnn.keras"

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

    return log_mel


# ---------------------------------------------------------
# Build NumPy dataset
# ---------------------------------------------------------

def build_split(df, split_name):
    split_df = df[
        df["split"] == split_name
    ].reset_index(drop=True)

    features = []
    labels = []

    total = len(split_df)

    print(
        f"\nProcessing {split_name}: "
        f"{total} samples"
    )

    for index, row in split_df.iterrows():

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
            (index + 1) % 250 == 0
            or index + 1 == total
        ):
            print(
                f"  {index + 1}/{total}"
            )

    X = np.array(
        features,
        dtype=np.float32
    )

    y = np.array(
        labels,
        dtype=np.int64
    )

    # Add CNN channel dimension
    X = X[..., np.newaxis]

    return X, y


# ---------------------------------------------------------
# Feature normalization
# ---------------------------------------------------------

def normalize_data(
    X_train,
    X_validation,
    X_test
):
    mean = np.mean(X_train)
    std = np.std(X_train)

    print(
        f"\nTraining feature mean: "
        f"{mean:.4f}"
    )

    print(
        f"Training feature std: "
        f"{std:.4f}"
    )

    X_train = (
        X_train - mean
    ) / (std + 1e-8)

    X_validation = (
        X_validation - mean
    ) / (std + 1e-8)

    X_test = (
        X_test - mean
    ) / (std + 1e-8)

    return (
        X_train,
        X_validation,
        X_test
    )


# ---------------------------------------------------------
# CNN model
# ---------------------------------------------------------

def build_model(input_shape):
    model = models.Sequential(
        [
            layers.Input(
                shape=input_shape
            ),

            layers.Conv2D(
                32,
                kernel_size=(3, 3),
                activation="relu",
                padding="same"
            ),

            layers.BatchNormalization(),

            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),

            layers.Conv2D(
                64,
                kernel_size=(3, 3),
                activation="relu",
                padding="same"
            ),

            layers.BatchNormalization(),

            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),

            layers.Conv2D(
                128,
                kernel_size=(3, 3),
                activation="relu",
                padding="same"
            ),

            layers.BatchNormalization(),

            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),

            layers.GlobalAveragePooling2D(),

            layers.Dropout(0.35),

            layers.Dense(
                128,
                activation="relu"
            ),

            layers.Dropout(0.30),

            layers.Dense(
                len(LABELS),
                activation="softmax"
            )
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

def evaluate_model(
    model,
    X_test,
    y_test
):
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

    print(
        f"\nTest accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"Test macro F1: "
        f"{macro_f1:.4f}"
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
        "Confusion matrix:\n"
    )

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found:\n"
            f"{METADATA_FILE}"
        )

    df = pd.read_csv(
        METADATA_FILE
    )

    print(
        "Building CREMA-D speech dataset..."
    )

    X_train, y_train = build_split(
        df,
        "train"
    )

    X_validation, y_validation = (
        build_split(
            df,
            "validation"
        )
    )

    X_test, y_test = build_split(
        df,
        "test"
    )

    print(
        "\nDataset shapes:"
    )

    print(
        f"Train: "
        f"{X_train.shape}, {y_train.shape}"
    )

    print(
        f"Validation: "
        f"{X_validation.shape}, "
        f"{y_validation.shape}"
    )

    print(
        f"Test: "
        f"{X_test.shape}, {y_test.shape}"
    )

    (
        X_train,
        X_validation,
        X_test
    ) = normalize_data(
        X_train,
        X_validation,
        X_test
    )

    model = build_model(
        X_train.shape[1:]
    )

    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6
        )
    ]

    print(
        "\nStarting training..."
    )

    model.fit(
        X_train,
        y_train,
        validation_data=(
            X_validation,
            y_validation
        ),
        epochs=30,
        batch_size=32,
        callbacks=callbacks
    )

    MODEL_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    model.save(
        MODEL_OUTPUT
    )

    print(
        f"\nModel saved to: "
        f"{MODEL_OUTPUT.resolve()}"
    )

    evaluate_model(
        model,
        X_test,
        y_test
    )


if __name__ == "__main__":
    main()