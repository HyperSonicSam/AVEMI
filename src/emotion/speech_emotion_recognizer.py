import json
from pathlib import Path

import librosa
import numpy as np
import tensorflow as tf


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "speech_emotion_cnn.keras"
)

CONFIG_PATH = (
    PROJECT_ROOT
    / "models"
    / "speech_emotion_config.json"
)


# ---------------------------------------------------------
# Load configuration
# ---------------------------------------------------------

with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)


SAMPLE_RATE = CONFIG["sample_rate"]
DURATION = CONFIG["duration"]
N_MELS = CONFIG["n_mels"]
N_FFT = CONFIG["n_fft"]
HOP_LENGTH = CONFIG["hop_length"]
TARGET_SAMPLES = CONFIG["target_samples"]

FEATURE_MEAN = CONFIG["feature_mean"]
FEATURE_STD = CONFIG["feature_std"]

LABELS = CONFIG["labels"]


# ---------------------------------------------------------
# Load trained model
# ---------------------------------------------------------

emotion_model = tf.keras.models.load_model(
    MODEL_PATH
)


# ---------------------------------------------------------
# Audio preprocessing
# ---------------------------------------------------------

def _load_audio(audio_path):
    """
    Load an audio file using the same settings used during
    CREMA-D model training.
    """

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


def _create_log_mel(audio):
    """
    Convert an audio waveform into the same Log-Mel
    representation used during model training.
    """

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


def _prepare_input(audio_path):
    """
    Prepare one audio recording for CNN inference.
    """

    audio = _load_audio(
        audio_path
    )

    log_mel = _create_log_mel(
        audio
    )

    # Apply training-set normalization.
    log_mel = (
        log_mel - FEATURE_MEAN
    ) / (FEATURE_STD + 1e-8)

    # Add channel dimension.
    log_mel = log_mel[..., np.newaxis]

    # Add batch dimension.
    log_mel = log_mel[np.newaxis, ...]

    return log_mel.astype(
        np.float32
    )


# ---------------------------------------------------------
# Emotion prediction
# ---------------------------------------------------------

def predict_emotion(audio_path):
    """
    Predict emotion from a speech recording.

    Returns:
        dict containing:
            emotion
            confidence
            probabilities
    """

    model_input = _prepare_input(
        audio_path
    )

    predictions = emotion_model.predict(
        model_input,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    emotion = LABELS[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    probabilities = {
        label: float(probability)
        for label, probability
        in zip(LABELS, predictions)
    }

    return {
        "emotion": emotion,
        "confidence": confidence,
        "probabilities": probabilities
    }