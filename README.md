<div align="center">

# 🎙️ Production Real-Time Voice AI Agent

### A High-Performance, Low-Latency Multi-Turn Conversational Voice Assistant
Powered by **SpeechRecognition (STT)**, **Groq Cloud LPUs (`qwen/qwen3.8-27b`)**, and **Local Offline Text-To-Speech (TTS)**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20LPU-f55036.svg)](https://groq.com/)
[![Speech](https://img.shields.io/badge/Audio-PyAudio%20%7C%20SpeechRecognition-green.svg)](https://pypi.org/project/SpeechRecognition/)
[![TTS](https://img.shields.io/badge/TTS-pyttsx3%20Offline-orange.svg)](https://pypi.org/project/pyttsx3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

</div>

## 📖 Overview

This repository houses a **production-ready, real-time Voice AI Agent** engineered for low-latency conversational audio loops. Unlike traditional chatbot implementations, this assistant enables full duplex voice dialogue: listening through your microphone, reasoning with high-speed LLMs on Groq LPUs, and responding aloud using local text-to-speech.

### 🌟 Key Highlights:
- **⚡ Ultra-Low Latency:** Leverages Groq's Language Processing Units (LPUs) to generate conversational responses in **sub-400ms**.
- **💰 100% Free Voice Stack:** Zero paid OpenAI credits required. Combines free Groq API tiers with local, offline TTS synthesis.
- **🧠 Multi-Turn Conversational Memory:** Maintains an adaptive sliding-window dialogue buffer, enabling context-aware follow-up questions.
- **🛡️ Adaptive Noise Calibration:** Dynamically calibrates ambient acoustic room noise to eliminate phantom speech triggers and keyboard clicks.
- **🧩 Clean Modular Architecture:** Decoupled `stt`, `llm`, and `tts` sub-modules conforming to SOLID design principles.

---

## 🏛️ System Architecture

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant Mic as 🎙️ Microphone
    participant STT as 🔍 STT Engine (Google Speech)
    participant Agent as 🧠 Voice Orchestrator
    participant Groq as ⚡ Groq Cloud LPU (Qwen 27B)
    participant TTS as 🔊 pyttsx3 Engine (Offline SAPI5)

    User->>Mic: Speaks audio ("What is quantum computing?")
    Mic->>STT: Raw PCM Audio Stream
    STT->>Agent: Transcribed Text
    Note over Agent: Validates input & checks exit commands
    Agent->>Groq: Prompt + Sliding Conversation History
    Groq-->>Agent: AI Completion (< 400ms)
    Note over Agent: Updates multi-turn dialogue buffer
    Agent->>TTS: Text payload
    TTS->>User: Audio playback through speakers
```

---

## 📂 Project Structure

```text
Voice_Agent/
│
├── core/
│   ├── __init__.py           # Package namespace definition
│   ├── stt.py                # Speech-to-Text audio capture & calibration
│   ├── tts.py                # Offline Text-to-Speech synthesis engine
│   └── llm.py                # Conversational manager & Groq API client
│
├── config.py                 # Centralized environment & settings management
├── agent.py                  # VoiceAgent pipeline orchestrator
├── main.py                   # Interactive CLI application with Rich UI
├── requirements.txt          # Production-pinned Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusion rules (protects credentials)
├── LICENSE                   # Open-source MIT License
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10 or higher**
- A working microphone and speaker setup
- A free **Groq API Key** (available at [console.groq.com](https://console.groq.com))

### 2. Clone the Repository
```bash
git clone https://github.com/Rohit18457/voice-ai-agent.git
cd voice-ai-agent
```

### 3. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Windows PyAudio Tip:** If you encounter compiler errors installing `pyaudio`, install the pre-compiled wheel via:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

> **Linux Note:** Linux users need `portaudio` and `espeak`:
> ```bash
> sudo apt-get update && sudo apt-get install -y portaudio19-dev espeak ffmpeg
> ```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```

### 6. Run the Voice Agent
```bash
python main.py
```

---

## 💬 Example Interactive Walkthrough

```text
============================================================
🎙️ Production Voice AI Agent
Real-Time Conversational Loop: STT -> Groq LPU (qwen/qwen3.8-27b) -> Local TTS
Features: Multi-turn context | Latency logging | Adaptive noise calibration
Say 'exit', 'quit', or 'bye' to terminate session.
============================================================

✓ Microphone calibrated and ready.

Listening... Speak into your microphone:
You: Who was Alan Turing?
AI (320ms latency): Alan Turing was a pioneering British mathematician and computer scientist who played a pivotal role in cracking intercepted coded messages during World War Two, and is widely considered the father of theoretical computer science and artificial intelligence.
[🔊 Spoken aloud through speakers]

Listening... Speak into your microphone:
You: What was the name of his test for machine intelligence?
AI (295ms latency): It is called the Turing Test, originally introduced by him as the "Imitation Game" in 1950 to evaluate whether a machine can exhibit intelligent behavior indistinguishable from that of a human.
[🔊 Spoken aloud through speakers]

Listening... Speak into your microphone:
You: Goodbye!
AI: Goodbye! Have a wonderful day!
Voice session ended.
```

---

## 💡 Engineering Highlights & Interview Q&A

### 1. Why use Groq LPUs instead of traditional GPUs?
Standard cloud GPU endpoints (e.g. standard OpenAI or self-hosted vLLM) typically introduce **1,500ms to 3,000ms** of Time-To-First-Token (TTFT) latency for 27B+ parameter models. In voice interaction, delays over 1 second break the illusion of real-time dialogue. Groq's deterministic LPU architecture delivers token generation speeds exceeding **400 tokens/second**, achieving **sub-400ms end-to-end latency**.

### 2. Why offline local TTS instead of cloud audio synthesis?
Cloud TTS services (ElevenLabs, OpenAI TTS) introduce round-trip network hops and rate limits. By utilizing `pyttsx3` with Windows SAPI5 / Linux eSpeak, speech synthesis executes instantaneously on the host CPU with **0ms API overhead** and **zero recurring costs**.

### 3. How is context managed across long conversations?
The `ConversationalAgent` class implements a sliding-window message queue (`max_history_turns=6`). Older user/assistant dialogue turns are automatically pruned while strictly preserving the initial `SYSTEM_PROMPT`. This bounds memory footprint and eliminates context overflow errors.

---

## ⚙️ Configuration Reference

All settings can be customized in `.env` without modifying source code:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | *(Required)* | Your Groq Cloud API authentication key |
| `GROQ_MODEL` | `qwen/qwen3.8-27b` | High-speed Groq conversational model |
| `CALIBRATION_DURATION` | `1.0` | Seconds spent measuring ambient background noise |
| `PAUSE_THRESHOLD` | `1.5` | Silence duration in seconds indicating end of speech |
| `ENERGY_THRESHOLD` | `300` | Microphone sensitivity threshold (0 for auto) |
| `TTS_RATE` | `175` | Speech speed in words per minute |
| `TTS_VOLUME` | `1.0` | Output speech volume (0.0 to 1.0) |
| `TTS_VOICE_INDEX` | `0` | System voice index (0 for male, 1 for female) |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/NewFeature`).
3. Commit your Changes (`git commit -m 'feat: Add NewFeature'`).
4. Push to the Branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

<div align="center">
Built with ❤️ for real-time AI and conversational systems.
</div>

