# Emotion-Aware In-Vehicle Conversational Assistant

An MSc Artificial Intelligence and Machine Learning project exploring the use of emotion-aware conversational AI within an in-vehicle environment.

## Overview

This project investigates how a conversational AI assistant can adapt its behaviour based on the emotional state of a vehicle occupant.

The system is designed as an interactive in-vehicle assistant capable of understanding natural-language requests, maintaining a simulated vehicle state, and performing actions such as:

- Controlling music
- Adjusting vehicle temperature
- Setting navigation destinations
- Adapting responses and actions according to the user's emotional state

The project compares a **baseline conversational assistant** with an **emotion-aware assistant** to investigate how emotional context can influence interaction and system behaviour.

## Current Prototype

The current demonstrator is built using Python and Streamlit.

The prototype currently includes:

- Interactive conversational interface
- Simulated vehicle state
- Natural-language intent detection
- Music control
- Temperature control
- Navigation control
- Simulated driver emotion selection
- Emotion confidence values
- Baseline and Emotion-Aware operating modes
- Emotion-specific behavioural profiles

## System Architecture

The project is being developed using a modular architecture:

```text
User Interaction
       |
       v
Streamlit Interface
       |
       +------------------+
       |                  |
       v                  v
Intent Router       Emotion Manager
       |                  |
       |            Emotion Profile
       |                  |
       +--------+---------+
                |
                v
         Action Manager
                |
                v
       Simulated Vehicle State