# 🥦 Smart Fridge Chef: Multimodal AI Agent

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Inference-Groq_LPU-orange?style=for-the-badge)](https://groq.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org/)

> **"Industrial Computer Vision applied to a Consumer Problem."**

## 🚀 The Problem
In my PhD research (Manufacturing AI), I use Computer Vision to detect material defects. I realized the same logic could solve a daily problem: **Food Waste & Decision Fatigue.**
Instead of detecting cracks in steel, this agent detects ingredients in a fridge and "manufactures" a culinary plan.

## 🧠 Architecture
This project implements a **Multimodal Agentic Workflow**:

* **Visual Perception (The Eyes):** Llama 4 Scout (17B) scans the image to extract a structured list of ingredients.
* **Reasoning Engine (The Brain):** Llama 3.3 (70B) uses the ingredient list + pantry assumptions to generate valid recipes.
* **Frontend:** Streamlit single-page application for rapid visual feedback.

## 🛠️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Durgaprasadpenumuru/smart-fridge-agent.git
cd smart-fridge-agent
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up API Key: Create a file named .env and add your key:
```bash
GROQ_API_KEY=gsk_your_key_here
```
### 4. Run the App
```bash
streamlit run chefassistant.py
```
---
## 👨‍💻 Author
**Dr. Durgaprasad Penumuru**




