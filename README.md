# AVEMI

**Affective Vehicle Emotion-aware Multimodal Intelligence**

AVEMI is an emotion-aware in-vehicle conversational assistant developed as part of an MSc Artificial Intelligence and Machine Learning project at the University of Birmingham.

The system explores how emotional context can be incorporated into an in-vehicle conversational assistant while maintaining reliable and deterministic vehicle-related actions.

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
- Vehicle-state queries including:
  - Fuel level
  - Cabin temperature
  - Music status
  - Navigation status
  - Current destination
- Text-based interaction
- Voice input using Faster-Whisper
- Voice output using Piper TTS
- Interactive Streamlit dashboard
- Animated AVEMI HUD interface

---

## System Overview

AVEMI separates conversational reasoning from vehicle-control logic.

Natural-language input is interpreted into structured commands. Vehicle actions and factual vehicle-state queries are handled deterministically, while general conversational requests are processed by the local language model.

This design helps reduce hallucination when AVEMI interacts with vehicle-related information.

---

## Vehicle State

The current prototype simulates several vehicle properties:

- Cabin temperature
- Fuel level
- Music status
- Music category
- Navigation state
- Destination

These states are updated dynamically as AVEMI executes supported commands.

---

## Emotion-Aware Interaction

AVEMI currently supports two operating modes.

### Baseline

The assistant operates without emotional adaptation.

### Emotion-Aware

A simulated driver emotional state and confidence value are provided to AVEMI and used to adapt conversational responses and supported behaviour.

Current simulated emotions include:

- Neutral
- Happy
- Sad
- Angry
- Stressed
- Tired

Automatic emotion recognition is planned as the next major development phase.

---

## Voice Interaction

AVEMI supports two-way voice interaction.

### Speech-to-Text

Voice input is transcribed locally using Faster-Whisper.

### Text-to-Speech

Assistant responses are converted to speech using Piper TTS.

The interface uses a push-to-record microphone control:

1. Press the microphone button to begin recording.
2. Press again to stop recording.
3. The recorded audio is transcribed.
4. The transcribed message is automatically submitted to AVEMI.

---

## Technology Stack

- Python
- Streamlit
- Qwen
- Ollama
- Faster-Whisper
- Piper TTS
- streamlit-mic-recorder

---

## Project Structure

```text
AVEMI
│
├── app.py
│
├── src
│   ├── emotion
│   │   └── emotion_manager.py
│   │
│   ├── intents
│   │   └── intent_router.py
│   │
│   ├── llm
│   │   ├── command_parser.py
│   │   ├── ollama_client.py
│   │   └── prompt_builder.py
│   │
│   ├── speech
│   │   ├── speech_to_text.py
│   │   └── text_to_speech.py
│   │
│   └── vehicle
│       └── action_manager.py
│
└── README.md
```

---

## Running the Application

Create and activate a Python virtual environment and install the required dependencies.

Ensure that Ollama is running and that the required Qwen model is available locally.

Start AVEMI with:

```bash
streamlit run app.py
```

The application will open in the browser.

---

## Current Development Stage

The current version provides a functional end-to-end prototype with:

- Local LLM conversation
- Deterministic vehicle actions
- Vehicle-state queries
- Emotion-aware response adaptation
- Voice input and output
- Interactive dashboard interface

---

## Next Development Phase

The next phase of the project will focus on:

- Selecting appropriate emotion-recognition datasets
- Developing automatic emotion-recognition models
- Integrating detected emotion into AVEMI
- Creating a structured evaluation dataset
- Comparing Baseline and Emotion-Aware performance
- Measuring response quality, action accuracy, and emotional appropriateness
- Conducting experimental evaluation for the MSc dissertation

---

## Research Goal

The broader research goal is to investigate whether incorporating driver emotional context can improve the appropriateness and usefulness of an in-vehicle conversational assistant compared with an emotion-agnostic baseline.