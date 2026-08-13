# Emotion-Aware In-Vehicle Conversational Assistant

An MSc Artificial Intelligence and Machine Learning research project exploring the use of local language models and emotion-aware decision making in an in-vehicle conversational assistant.

The project investigates how a conversational assistant can interpret natural-language requests, incorporate driver emotional context, and adapt non-driving vehicle interactions such as music selection, climate control, and navigation.

## Current Prototype

The current implementation provides an interactive Streamlit-based vehicle assistant with:

- Natural-language conversation
- Local LLM inference using Ollama
- Structured command interpretation
- Simulated driver emotion
- Baseline and Emotion-Aware operating modes
- Emotion-adaptive music selection
- Climate control
- Navigation simulation
- Simulated vehicle state
- Rule-based fallback intent detection

## Current Model

The prototype currently uses:

**Qwen3 4B Instruct via Ollama**

The model runs locally and is used for:

1. Interpreting natural-language input into structured vehicle commands.
2. Generating short conversational responses.

The model can be replaced without changing the overall system architecture, allowing different local language models to be evaluated.

## System Architecture

The current pipeline is:

User Input  
↓  
Local LLM Command Parser  
↓  
Structured Command  
↓  
Vehicle Action Manager  
↓  
Vehicle State Update  
↓  
Emotion-Aware Prompt Construction  
↓  
Local LLM Response Generation  
↓  
Assistant Response

A deterministic action layer is maintained between the language model and the simulated vehicle state. The LLM interprets requests, while Python controls the execution of vehicle actions.

## Emotion-Aware Behaviour

The prototype currently supports the following simulated emotional states:

- Neutral
- Happy
- Sad
- Angry
- Stressed
- Tired

The interface provides two experimental modes:

### Baseline

The assistant performs tasks without using the simulated emotional state to adapt its behaviour.

### Emotion-Aware

The assistant receives emotional context and can adapt its responses and actions accordingly.

For example, the same request to play music can result in different music categories depending on the simulated emotional state.

## Supported Vehicle Interactions

The current prototype supports:

### Music

Examples:

- "Play some music."
- "Put something on."
- "I am stressed, play something relaxing."

### Climate Control

Examples:

- "Set the temperature to 20."
- "It is cold."
- "Make it warmer."
- "It is too hot."

### Navigation

Examples:

- "Take me home."
- "Navigate home."
- "Give me directions home."

The language model converts natural-language requests into structured commands before they are executed by the vehicle action manager.

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen3 4B Instruct
- JSON-based emotion profiles

## Project Structure

```text
sxb2022/
├── assets/
├── data/
│   └── emotion_profiles.json
├── src/
│   ├── core/
│   ├── emotion/
│   │   └── emotion_manager.py
│   ├── intents/
│   │   └── intent_router.py
│   ├── llm/
│   │   ├── command_parser.py
│   │   ├── ollama_client.py
│   │   └── prompt_builder.py
│   ├── storage/
│   ├── utils/
│   └── vehicle/
│       └── action_manager.py
├── tests/
├── app.py
├── requirements.txt
└── README.md