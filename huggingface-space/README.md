---
title: 📊 PVB Flow - Product Vision Board to Mermaid
emoji: 📊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.0.0
app_file: app.py
pinned: false
license: mit
hardware: zero-gpu
short_description: Product Vision Board to Mermaid diagram generator
models:
- Qwen/Qwen3-VL-4B-Instruct
tags:
- product-management
- mermaid
- diagram-generation
- vision-board
- ai-powered
- qwen
- qwen3
- zero-gpu
---

# 📊 PVB Flow - Product Vision Board to Mermaid Diagram Generator

Transform your Product Vision Board JSON into professional, operational process Mermaid diagrams with AI-powered analysis.

## ⚡ Features

🤖 **AI-Powered Generation**:
- **Qwen3-4B-Instruct**: State-of-the-art Qwen3 model optimized for instruction following
- **ZeroGPU Acceleration**: Fast inference with automatic GPU management
- **Operational Focus**: Creates process diagrams showing WHO does WHAT
- **Actor-Based Design**: Identifies systems, humans, and AI actors
- **Decision Points**: Shows branching logic and validation loops

🎯 **Smart Diagram Design**:
- **Process Workflows**: Sequential operational steps
- **Data Flows**: Input/output transformations
- **Validation Loops**: Error handling and enrichment
- **Visual Styling**: Color-coded actors and decision points

📊 **Interactive Features**:
- **Conversational Refinement**: Chat to improve diagrams
- **Layout Control**: Request vertical/horizontal layouts
- **Visual Enhancements**: Add colors, icons, subgraphs
- **Shareable Links**: Generate Mermaid Live Editor URLs

🔗 **Export Options**:
- **Mermaid Live Editor**: Direct link to edit and export
- **PNG/SVG/PDF Export**: Via Mermaid Live Editor
- **Share with Team**: Shareable links for collaboration

## 🚀 How to Use

### Basic Usage
1. **Paste Product Vision Board JSON** in the chat input
2. **Wait for diagram generation** (appears in right panel)
3. **Refine via chat** (e.g., "make it more vertical", "add colors")
4. **Generate shareable link** to open in Mermaid Live Editor

### Example Product Vision Board JSON
```json
{
  "1. Utilisateur Cible": [
    "Passionnés de cuisine amateur",
    "Professionnels de la restauration"
  ],
  "2. Description du Produit": [
    "Application de gestion de recettes avec suggestions personnalisées",
    "Planification automatique des repas de la semaine"
  ],
  "3. Fonctionnalités Clés": [
    "Recherche de recettes par ingrédients disponibles",
    "Génération automatique de liste de courses",
    "Suggestions basées sur les préférences alimentaires"
  ],
  "4. Enjeux et Indicateurs": [
    "Réduire le gaspillage alimentaire de 30%",
    "Atteindre 100 000 utilisateurs actifs en 6 mois"
  ],
  "Summary": "Simplifier la planification des repas et réduire le gaspillage alimentaire"
}
```

### Refinement Examples
- "Make it more vertical"
- "Add more colors to distinguish actors"
- "Simplify the diagram"
- "Add icons or emojis"
- "Show this as a swimlane diagram"

## 🎯 Perfect For

- **Product Managers**: Visualize product vision as operational processes
- **Business Analysts**: Transform requirements into process flows
- **Development Teams**: Understand operational workflows
- **Stakeholders**: Share vision in visual format
- **Documentation**: Professional process diagrams

## 🔧 Configuration

The app uses ZeroGPU for acceleration:
- No API key required
- Runs on Hugging Face ZeroGPU infrastructure
- Automatic model loading and GPU management

## 🔒 Privacy & Security

- **ZeroGPU**: Temporary GPU allocation per request
- **No Data Retention**: Vision boards processed temporarily
- **Secure Processing**: HF Spaces environment
- **Open Source Model**: Qwen3-4B-Instruct

## 🔗 Related Links

- **Mermaid Live Editor**: https://mermaid.live/edit
- **Mermaid Documentation**: https://mermaid.js.org/
- **Qwen3-4B-Instruct**: https://huggingface.co/Qwen/Qwen3-4B-Instruct
- **ZeroGPU**: https://huggingface.co/docs/hub/spaces-zerogpu

Start transforming your Product Vision Boards into professional diagrams! 📊✨
