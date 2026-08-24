# AVEMI

**Affective Vehicle Emotion-aware Multimodal Intelligence**

AVEMI is an emotion-aware in-vehicle conversational assistant developed as part of an MSc Artificial Intelligence and Machine Learning project at the University of Birmingham.

The project investigates how driver emotional context can be incorporated into an in-vehicle conversational assistant while maintaining reliable and deterministic vehicle-related actions.

---

## Current Features

- Local conversational AI using Qwen through Ollama
- Baseline and Emotion-Aware operating modes
- Natural-language command interpretation
- Deterministic vehicle action execution
- Simulated vehicle-state management
- Climate control interaction
- Music playback, pause, and resume controls
- Navigation and destination management
- Vehicle-state queries
- Text-based interaction
- Voice input using Faster-Whisper
- Voice output using Piper TTS
- Speech emotion recognition using a CNN trained on CREMA-D
- Automatic integration of detected speech emotion into the assistant
- Interactive Streamlit dashboard
- Animated AVEMI HUD interface

---

## System Overview

AVEMI separates conversational reasoning, emotion recognition, and vehicle-control logic.

User input can be provided through text or speech. Spoken input is transcribed using Faster-Whisper and analysed by the speech emotion recognition component.

Natural-language requests are interpreted into structured commands. Supported vehicle actions and factual vehicle-state queries are handled deterministically, while general conversational requests are processed by the local language model.

In Emotion-Aware mode, emotional context is incorporated into the conversational pipeline so that responses can adapt to the driver's emotional state.

This architecture allows emotional adaptation while reducing the risk of language-model hallucination affecting vehicle-related operations.

---

## Vehicle State

The prototype simulates several vehicle properties:

- Cabin temperature
- Fuel level
- Music status
- Music category
- Navigation state
- Destination

These states are updated dynamically as AVEMI executes supported commands.

---

## Emotion-Aware Interaction

AVEMI supports two operating modes.

### Baseline

The assistant processes requests without using driver emotional context for response adaptation.

### Emotion-Aware

Driver emotional context is incorporated into the assistant's conversational response generation.

The interface also provides simulated emotion controls for controlled demonstrations and comparisons.

For voice interaction, AVEMI can automatically estimate emotion from recorded speech using the trained speech emotion recognition model.

---

## Speech Emotion Recognition

AVEMI includes a speech emotion recognition (SER) component trained using the CREMA-D dataset.

The current model recognises six emotion classes:

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad

Audio is converted into fixed-size log-Mel spectrogram representations before being processed by a convolutional neural network (CNN).

### Dataset

CREMA-D contains 7,442 speech samples from 91 actors.

An actor-independent split is used to reduce speaker leakage:

- Training: 73 actors / 5,967 samples
- Validation: 9 actors / 737 samples
- Test: 9 actors / 738 samples

No actor appears across multiple dataset splits.

### Current Test Performance

The trained SER model achieved:

- Test accuracy: **52.17%**
- Macro F1-score: **0.5082**
- Weighted F1-score: **0.5066**

Detailed evaluation results and the confusion matrix are stored in the `evaluation/ser` directory.

---

## Voice Interaction

AVEMI supports two-way voice interaction.

### Speech-to-Text

Voice input is transcribed locally using Faster-Whisper.

### Speech Emotion Recognition

Recorded speech is processed by the trained SER model to estimate the driver's emotional state and associated confidence.

### Text-to-Speech

Assistant responses are converted to speech using Piper TTS.

The interface uses a push-to-record microphone control:

1. Press the microphone button to begin recording.
2. Press again to stop recording.
3. The recorded speech is transcribed.
4. Speech emotion is estimated.
5. The transcribed request is submitted to AVEMI.
6. In Emotion-Aware mode, the detected emotional context can influence the conversational response.

---

## Technology Stack

- Python
- Streamlit
- Qwen
- Ollama
- Faster-Whisper
- Piper TTS
- TensorFlow / Keras
- Librosa
- NumPy
- Pandas
- scikit-learn
- Matplotlib
- SoundFile
- streamlit-mic-recorder
- FFmpeg

---

## Project Structure

```text
AVEMI/
|
|-- app.py
|-- requirements.txt
|-- README.md
|
|-- data/
|   |-- crema_metadata.csv
|   `-- README.md
|
|-- models/
|   |-- speech_emotion_cnn.keras
|   `-- speech_emotion_config.json
|
|-- src/
|   |-- emotion/
|   |   |-- emotion_manager.py
|   |   `-- speech_emotion_recognizer.py
|   |
|   |-- intents/
|   |   `-- intent_router.py
|   |
|   |-- llm/
|   |   |-- command_parser.py
|   |   |-- ollama_client.py
|   |   `-- prompt_builder.py
|   |
|   |-- speech/
|   |   |-- speech_to_text.py
|   |   `-- text_to_speech.py
|   |
|   `-- vehicle/
|       `-- action_manager.py
|
|-- scripts/
|   |-- prepare_crema.py
|   |-- test_speech_emotion.py
|   `-- evaluate_speech_emotion.py
|
`-- evaluation/
    `-- ser/
        |-- ser_results.json
        `-- ser_confusion_matrix.png
```

---

## Dataset Setup

The raw CREMA-D dataset is not included in this repository.

The project uses the `AudioWAV` portion of CREMA-D.

Dataset metadata and the fixed actor-independent train/validation/test split are stored in:

```text
data/crema_metadata.csv
```

The location of the local CREMA-D dataset can be configured using the `CREMA_ROOT` environment variable.

Further information is provided in:

```text
data/README.md
```

---

## Installation

Create and activate a Python virtual environment.

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

FFmpeg must also be installed separately and available from the system command line.

Verify the installation with:

```bash
ffmpeg -version
```

Ollama must be installed and running with the required Qwen model available locally.

---

## Running AVEMI

Start the application with:

```bash
streamlit run app.py
```

The AVEMI dashboard will open in the browser.

---

## Speech Emotion Evaluation

The trained speech emotion recognition model can be independently evaluated using:

```bash
python scripts/evaluate_speech_emotion.py
```

The evaluation calculates:

- Test accuracy
- Per-class precision
- Per-class recall
- Per-class F1-score
- Macro F1-score
- Weighted F1-score
- Confusion matrix

Evaluation outputs are saved under:

```text
evaluation/ser/
```

---

## Current Development Stage

The current AVEMI prototype provides an end-to-end implementation incorporating:

- Local LLM-based conversation
- Deterministic vehicle actions
- Vehicle-state queries
- Baseline and Emotion-Aware interaction modes
- Speech-to-text
- Text-to-speech
- Automatic speech emotion recognition
- Emotion-aware response adaptation
- Interactive vehicle dashboard
- Independent SER evaluation

The current automatic emotion-recognition implementation focuses on the **speech modality**. AVEMI retains a multimodal research architecture, while additional modalities such as visual driver-state recognition are outside the implemented scope of the current prototype.

---

## Research Goal

The broader research goal is to investigate whether incorporating driver emotional context can improve the appropriateness and usefulness of an in-vehicle conversational assistant compared with an emotion-agnostic baseline.

The prototype provides the technical framework for comparing baseline and emotion-aware behaviour while separately evaluating the performance and limitations of automatic speech emotion recognition.