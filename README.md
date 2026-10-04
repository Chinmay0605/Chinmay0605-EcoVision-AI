# 🌱 EcoVision AI

### Intelligent Waste Analysis & Responsible Disposal Platform

> **See your waste. Understand it. Dispose responsibly.**

EcoVision AI is an AI-powered waste analysis platform that uses computer vision to identify household waste, determine its material and recyclability, provide responsible disposal recommendations, and generate city-specific disposal guidance and PDF reports.

The platform combines a **React frontend**, **FastAPI backend**, **local CLIP vision model**, multiple intelligent agents, **SQLite scan history**, analytics, and downloadable reports into a complete waste-management assistant.

---

## ✨ Features

### 🤖 AI Waste Detection
- Upload an image of waste
- AI-powered image classification using OpenAI CLIP
- Zero-shot classification without requiring a custom trained dataset
- Confidence score for every prediction
- Alternative predictions displayed to the user

### ♻️ Waste Classification
EcoVision AI can identify categories such as:

- Plastic
- Paper
- Cardboard
- Glass
- Metal
- Organic Waste
- E-Waste
- Textile
- Hazardous Waste
- General Household Waste

### 🌍 Responsible Disposal Recommendations

For every detected waste item, the system provides:

- Recommended waste bin
- Disposal instructions
- Safe handling instructions
- Eco-friendly tips
- Recyclability information

### 📍 City-Specific Disposal Intelligence

Users can select a city and receive location-aware disposal guidance.

Currently supported:

- 🇮🇳 Indore
- 🇮🇳 Bhopal
- 🇮🇳 Delhi
- 🇮🇳 Mumbai

The selected location can also be chosen individually for previous scans when generating reports.

### 📊 Analytics Dashboard

The dashboard provides:

- Total scans
- Recyclable scans
- Non-recyclable scans
- Average AI confidence
- Recyclability percentage
- AI performance overview
- Scan history

### 📄 PDF Reports

Generate professional waste-analysis reports containing:

- Scan information
- Detected waste
- Material
- Confidence
- Recyclability
- Disposal recommendations
- City-specific disposal guidance
- Important disposal notes

### 🗂️ Scan History

Users can:

- View previous analyses
- View detected categories
- See confidence scores
- Select a city for an individual scan
- Generate reports for previous scans
- Delete individual scans
- Delete complete scan history

---

# 🧠 System Architecture

```text
                         ┌─────────────────────┐
                         │    Waste Image      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Vision Agent     │
                         │   CLIP Zero-Shot    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │    Classification Agent    │
                    │ Category • Material •       │
                    │ Recyclability                │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │   Knowledge Agent   │
                         │ Disposal Knowledge  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │   Recommendation Agent      │
                    │ Bin • Disposal • Handling   │
                    │ Eco Tips                    │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │   Disposal Intelligence    │
                    │      City-Specific          │
                    └──────────────┬──────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 ▼                 ▼                 ▼
        ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
        │ Web Dashboard  │ │ PDF Reports  │ │ Scan History  │
        └────────────────┘ └──────────────┘ └───────────────┘