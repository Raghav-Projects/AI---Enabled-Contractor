# AI---Enabled-Contractor
AI-powered construction estimator that provides real-time material pricing and budget plans.

 🏗️ AI Smart Contractor & Site Manager

An AI-powered General Contractor that helps you plan, budget, and manage construction projects.

This application acts as an autonomous site manager capable of analyzing blueprints, estimating real-time material costs using Google Search, and answering voice commands. It leverages **Google Gemini 2.5 Flash-Lite** for multimodal reasoning (text, voice, and vision).

 🎥 Project Demo
[Demo Preview](https://drive.google.com/file/d/1h2tbvQze68sV6vdEAp6m3A-tKfRMkZpO/view?usp=sharing)

 🌟 Key Features
* 5-in-1 AI Persona: Acts as a Manager, Architect, Estimator, Compliance Officer, and Logistics Coordinator.
* Real-Time Market Pricing: Uses **Google Search Grounding** to fetch live prices for cement, steel, bricks, etc., instead of hallucinating numbers.
* Blueprint Analysis: Upload images/blueprints, and the AI will analyze dimensions and material requirements.
* Voice-Enabled: Talk to your contractor using the built-in microphone feature.
* Multimodal: Processes Text, Images, and Audio simultaneously.

🛠️ Tech Stack
* Frontend:[Streamlit](https://streamlit.io/)
* AI Model: Google Gemini 2.5 Flash-Lite
* Audio Processing:`streamlit-mic-recorder`
* Image Processing: Pillow (PIL)
* API Integration: `google-genai` SDK

 🚀 Installation & Setup

 1. Clone the Repository
```bash
git clone [https://github.com/Raghav-Projects/AI---Enabled-Contractor.git](https://github.com/Raghav-Projects/AI---Enabled-Contractor.git)
cd AI---Enabled-Contractor
