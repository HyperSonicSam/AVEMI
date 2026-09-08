# AVEMI

**Affective Vehicle Emotion-Aware Multimodal Intelligence**

AVEMI is an experimental emotion-aware in-vehicle conversational assistant developed as an MSc Artificial Intelligence and Machine Learning project at the University of Birmingham.

It explores a simple question: **can estimated emotional context make an in-vehicle assistant more context-aware without sacrificing predictable vehicle functionality?**

The prototype combines local speech recognition, speech emotion recognition, local LLM-based conversation, text-to-speech and deterministic simulated vehicle controls in a single Streamlit application.

> **Project status:** Research prototype / proof of concept. AVEMI is not a production vehicle-control system and has not been validated for safety-critical use.

---

## Highlights

- Fully local conversational AI using **Qwen3 4B through Ollama**
- **Baseline** and **Emotion-Aware** operating modes for comparison
- Voice input using **Faster-Whisper**
- Voice output using **Piper TTS**
- Six-class speech emotion recognition using a **CNN trained on CREMA-D**
- Log-Mel spectrogram acoustic features
- Deterministic handling of supported vehicle actions and state queries
- Simulated climate, music, navigation and vehicle-state functionality
- Streamlit dashboard with an animated AVEMI HUD
- Separation between generative conversation and vehicle-state control

---

## Architecture

AVEMI separates the system into three principal pathways:

1. **Acoustic pathway** — recorded speech is converted to a standard audio representation and analysed by the speech emotion recognition model.
2. **Conversational pathway** — transcribed or typed requests can be processed by Qwen through Ollama, with estimated emotional context supplied in Emotion-Aware mode.
3. **Deterministic vehicle pathway** — supported vehicle actions and state queries are handled by application logic rather than unrestricted LLM generation.

This separation allows emotional context to influence interaction while preventing an estimated emotion from overriding an explicit vehicle command or allowing the LLM to directly control the simulated vehicle state.

---

## Emotion-Aware Interaction

AVEMI supports two configurations:

### Baseline

The assistant processes the interaction without supplying the separately estimated speech-emotion state to the conversational adaptation layer.

### Emotion-Aware

The estimated emotional state can influence conversational style and selected context-sensitive behaviour. For example, a generic music request can select a different music category according to the supplied emotional context while retaining the same underlying `play_music` intent.

AVEMI treats emotion predictions as **uncertain contextual information**, not objective measurements of how a user actually feels.

---

## Speech Emotion Recognition

The SER component was trained on **CREMA-D**, which contains 7,442 recordings from 91 actors. The implementation predicts six classes:

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad

Audio is represented as fixed-size log-Mel spectrograms and classified using a convolutional neural network.

### Actor-independent split

| Split | Actors | Samples |
| --- | ---: | ---: |
| Training | 73 | 5,967 |
| Validation | 9 | 737 |
| Test | 9 | 738 |

No actor appears across multiple splits.

### Test performance

| Metric | Result |
| --- | ---: |
| Accuracy | **52.17%** |
| Macro F1 | **0.5082** |
| Weighted F1 | **0.5066** |

The results indicate moderate recognition capability rather than production-grade emotion detection. Performance also varies substantially by emotional class. Detailed evaluation outputs are available under `evaluation/ser/`.

---

## Integrated Evaluation

The complete prototype was evaluated using **31 predefined interaction cases**.

- **19/19 tested vehicle-related intents** were correctly identified.
- **2/2 tested unsupported vehicle operations** were correctly rejected.
- Emotion-aware context produced observable changes in selected conversational responses and context-sensitive behaviour.

These figures describe the defined evaluation set only. They are **not evidence of universal reliability, real-vehicle safety, or statistically validated improvements in perceived interaction quality**. The project did not include a formal human-participant study.

---

## Simulated Vehicle Functionality

The prototype maintains state for representative in-vehicle functions including:

- Cabin temperature
- Fuel level
- Music playback and category
- Navigation status
- Destination

Explicit supported operations are routed through deterministic application logic. Open-ended conversation is handled separately by the local language model.

---

## Technology Stack

- Python
- Streamlit
- Qwen3 4B
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
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── crema_metadata.csv
│   ├── emotion_profiles.json
│   └── README.md
├── models/
│   ├── speech_emotion_cnn.keras
│   └── speech_emotion_config.json
├── src/
│   ├── emotion/
│   ├── intents/
│   ├── llm/
│   ├── speech/
│   └── vehicle/
├── scripts/
└── evaluation/
    └── ser/
```

The raw CREMA-D media files and local Piper voice model are intentionally not included in the repository.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HyperSonicSam/AVEMI.git
cd AVEMI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install external components

AVEMI also requires:

- **FFmpeg**, available from the command line
- **Ollama**, running locally with the required Qwen3 4B model
- **Piper TTS** and a compatible local Piper voice model for spoken output

Verify FFmpeg with:

```bash
ffmpeg -version
```

The Piper voice model is deliberately excluded from Git because it is a large runtime asset. Configure/download the required Piper voice locally before enabling TTS.

---

## Dataset Setup

The raw **CREMA-D** dataset is not redistributed in this repository.

The project uses its `AudioWAV` recordings. Dataset metadata and the fixed actor-independent train/validation/test split are retained in:

```text
data/crema_metadata.csv
```

The local dataset location can be configured using the `CREMA_ROOT` environment variable. See `data/README.md` for the project-specific setup.

---

## Running AVEMI

With the dependencies and local models configured:

```bash
streamlit run app.py
```

The Streamlit interface will then open in the browser.

---

## Evaluating the SER Model

The trained speech emotion recognition model can be evaluated independently with:

```bash
python scripts/evaluate_speech_emotion.py
```

Evaluation outputs are stored under:

```text
evaluation/ser/
```

---

## Scope and Limitations

AVEMI is **multimodal at the interaction level**: it supports text and speech interaction alongside simulated vehicle context. The implemented automatic emotion-recognition component itself is currently **speech-only**; it does not fuse facial, physiological or other affective modalities.

Important limitations include:

- Moderate SER accuracy and class-dependent performance
- Training/evaluation on acted emotional speech rather than natural in-vehicle recordings
- Simulated rather than physical vehicle functionality
- Limited predefined system-level evaluation cases
- No formal human-participant evaluation of perceived empathy or appropriateness

Future work could investigate naturalistic in-vehicle speech, multimodal affect recognition, calibrated uncertainty handling, human evaluation and integration with a driving simulator or appropriately controlled vehicle interface.

---

## Academic Context

AVEMI was developed as an MSc Artificial Intelligence and Machine Learning project at the **University of Birmingham**.

The repository is maintained as a portfolio and research implementation of the prototype. The original academic evaluation and conclusions should be interpreted within the experimental scope and limitations described above.

---

## Author

**Samik Bhatia**

MSc Artificial Intelligence and Machine Learning  
University of Birmingham
