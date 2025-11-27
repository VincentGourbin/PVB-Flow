# 📊 PVB Flow - Product Vision Board to Mermaid Diagram Generator

Transform your Product Vision Board JSON into professional, operational process Mermaid diagrams with AI-powered analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator)

## 🎯 Overview

**PVB Flow** is an AI-powered tool that converts Product Vision Board JSON data into professional Mermaid diagrams. Unlike simple converters, it uses advanced language models to create **operational process flowcharts** that show WHO does WHAT, with decision points, validation loops, and visual styling.

### ✨ Key Features

- 🤖 **Dual Backend Support**:
  - **Local MLX**: Run on Apple Silicon (M1/M2/M3) with Qwen3 models
  - **HF Spaces**: Deploy on Hugging Face with ZeroGPU acceleration (Qwen3-VL-4B)

- 📊 **Smart Diagram Generation**:
  - Operational process workflows (not just conceptual structures)
  - Actor-based design (systems, humans, AI)
  - Decision points and branching logic
  - Data flows and transformations
  - Visual styling with colors and icons

- 🔗 **Mermaid Live Editor Integration**:
  - Generate shareable links to Mermaid Live Editor
  - Export diagrams as PNG, SVG, or PDF
  - Edit diagrams in real-time
  - Share with team members

- 💬 **Conversational Refinement**:
  - Chat-based interface for iterative improvements
  - Request layout changes (vertical/horizontal)
  - Add visual enhancements (colors, icons, subgraphs)
  - Simplify or expand diagrams

## 🚀 Quick Start

### Option 1: Use on Hugging Face Spaces (Recommended)

The easiest way to use PVB Flow:

👉 **[Try it now on Hugging Face Spaces](https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator)**

No installation required! Just paste your Product Vision Board JSON and start generating diagrams.

### Option 2: Run Locally (Apple Silicon)

For local usage on Mac M1/M2/M3:

```bash
# Clone the repository
git clone https://github.com/VincentGourbin/PVB-Flow.git
cd PVB-Flow

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Open `http://localhost:7860` in your browser.

## 📖 Usage

### Example Product Vision Board JSON

```json
{
  "1. Utilisateur Cible": [
    "Passionnés de cuisine amateur",
    "Professionnels de la restauration"
  ],
  "2. Description du Produit": [
    "Application de gestion de recettes",
    "Planification automatique des repas"
  ],
  "3. Fonctionnalités Clés": [
    "Recherche de recettes par ingrédients",
    "Génération automatique de liste de courses",
    "Suggestions personnalisées"
  ],
  "4. Enjeux et Indicateurs": [
    "Réduire le gaspillage alimentaire de 30%",
    "100 000 utilisateurs actifs en 6 mois"
  ],
  "Summary": "Simplifier la planification des repas"
}
```

### Workflow

1. **Paste JSON** → Chat input
2. **Wait for generation** → Diagram appears on right panel
3. **Refine via conversation**:
   - "Make it more vertical"
   - "Add more colors to distinguish actors"
   - "Simplify the diagram"
4. **Generate shareable link** → Open in Mermaid Live Editor

## 🏗️ Architecture

### Project Structure

```
PVB-Flow/
├── main.py                      # Local MLX entry point
├── requirements.txt             # Dependencies (MLX version)
├── LICENSE                      # MIT License
├── README.md                    # This file
│
├── src/pvb_flow/               # Main package
│   ├── ai/
│   │   ├── analyzer_factory.py      # Auto-detect backend
│   │   ├── mistral_mlx_analyzer.py  # MLX (Apple Silicon)
│   │   ├── mistral_text_analyzer.py # Transformers (cross-platform)
│   │   └── prompts_config.py        # System prompts
│   │
│   ├── ui/
│   │   ├── app.py                   # Gradio interface
│   │   └── handlers.py              # Event handlers
│   │
│   ├── core/
│   │   ├── mermaid_encoder.py       # URL encoding (fixed!)
│   │   └── mermaid_extractor.py     # Extract Mermaid code
│   │
│   └── utils/
│       └── json_validator.py        # Validate PVB JSON
│
└── huggingface-space/          # HF Spaces deployment
    ├── app.py                   # HF entry point
    ├── requirements.txt         # HF dependencies
    ├── README.md                # HF documentation
    ├── deploy.py                # Auto-deployment script
    │
    ├── src/
    │   ├── ai/
    │   │   └── qwen_zerogpu_analyzer.py  # Qwen3-VL + ZeroGPU
    │   ├── ui/
    │   │   └── spaces_interface.py       # Gradio for Spaces
    │   └── ... (shared modules)
    │
    └── Documentation/
        ├── QUICK_START.md       # 2-step deployment
        ├── DEPLOYMENT.md        # Full deployment guide
        ├── FINAL_CONFIG.md      # Technical details
        ├── ZEROGPU_MIGRATION.md # Migration guide
        └── QWEN3_SUMMARY.txt    # Visual summary
```

### Key Components

#### 1. AI Backends

| Backend | Platform | Model | Speed |
|---------|----------|-------|-------|
| **MLX** | Apple Silicon | Qwen3-8bit | ⚡ Very Fast |
| **Transformers** | Cross-platform | Mistral | 🐌 Slower |
| **ZeroGPU** | HF Spaces | Qwen3-VL-4B | ⚡ Fast |

#### 2. Prompt Engineering

Carefully crafted prompts generate:
- ✅ Operational process diagrams
- ✅ Actor identification
- ✅ Decision points and branching
- ✅ Data flows
- ✅ Visual styling

#### 3. Mermaid Integration

- **Encoder**: Generates Mermaid Live Editor URLs
  - Fixed encoding: `zlib.compress()` with header ✅
  - Base64url encoding
  - Shareable links

- **Extractor**: Parses Mermaid code from LLM responses
  - Validates syntax
  - Formats for display

## 🚀 Deployment to Hugging Face Spaces

Automated deployment in 2 steps:

```bash
# 1. Set HF token
export HF_TOKEN="hf_xxxxxxxxxxxxx"

# 2. Deploy
cd huggingface-space
python3 deploy.py
```

**Features**:
- ✅ Auto-creates Space with `hardware: zero-gpu`
- ✅ Uploads all files
- ✅ No API keys needed
- ✅ Model auto-downloads from HF Hub

See [huggingface-space/QUICK_START.md](./huggingface-space/QUICK_START.md)

## 📊 Models

### Local (MLX)
- **Model**: `mlx-community/Mistral-Small-3.1-24B-Instruct-2503-8bit`
- **Size**: 24B params, 8-bit quantized
- **Platform**: Apple Silicon only

### HF Spaces (ZeroGPU)
- **Model**: `Qwen/Qwen3-VL-4B-Instruct`
- **Size**: 4B params
- **Hardware**: ZeroGPU (T4/A10G)
- **No API key required** ✅

## 🔧 Configuration

### Local Version

No configuration needed! Auto-detects:
- ✅ Hardware (MLX/CUDA/MPS/CPU)
- ✅ Downloads models on first run
- ✅ Manages memory

### HF Spaces Version

Configured via `README.md` metadata:
```yaml
hardware: zero-gpu
models: [Qwen/Qwen3-VL-4B-Instruct]
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](./huggingface-space/QUICK_START.md) | 2-step deployment |
| [DEPLOYMENT.md](./huggingface-space/DEPLOYMENT.md) | Full deployment guide |
| [FINAL_CONFIG.md](./huggingface-space/FINAL_CONFIG.md) | Technical reference |
| [ZEROGPU_MIGRATION.md](./huggingface-space/ZEROGPU_MIGRATION.md) | Migration from API |
| [QWEN3_SUMMARY.txt](./huggingface-space/QWEN3_SUMMARY.txt) | Visual summary |

## 🐛 Troubleshooting

### Local (MLX)

**Model fails to load:**
- Ensure Apple Silicon (M1/M2/M3)
- Minimum 8GB RAM
- Try transformers backend

**Slow generation:**
- First run downloads models
- Subsequent runs much faster

### HF Spaces

**Space not starting:**
- Check logs for errors
- Ensure `hardware: zero-gpu` in README
- Verify model name

**Slow inference:**
- First request loads model (warmup)
- ZeroGPU timeout after 60s inactivity
- Model reloads on next request

## 🎯 Key Features Explained

### 1. Operational Process Focus

Unlike simple converters that create conceptual structures, PVB Flow generates:
- **WHO**: Different actors (System, AI, Human)
- **WHAT**: Specific actions and steps
- **WHEN**: Decision points and conditions
- **HOW**: Data flows and transformations

### 2. Mermaid Live Editor Integration

The fixed encoder (`mermaid_encoder.py`) now correctly:
- Uses `zlib.compress()` with header ✅
- Generates working URLs for Mermaid Live Editor
- Allows export to PNG/SVG/PDF
- Enables real-time editing

### 3. Conversational Refinement

Chat-based iteration:
- Natural language requests
- Layout adjustments
- Visual enhancements
- Diagram simplification

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit PR

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- **Qwen Team**: Excellent Qwen3 models
- **Hugging Face**: Spaces & ZeroGPU
- **Gradio**: Amazing UI framework
- **Mermaid.js**: Diagram syntax & editor

## 🔗 Links

- 🚀 [Live Demo (HF Spaces)](https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator)
- 📝 [Mermaid Live Editor](https://mermaid.live/edit)
- 🤖 [Qwen3-VL Model](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)
- 📖 [Mermaid Docs](https://mermaid.js.org/)

## 📧 Contact

Vincent Gourbin - [@VincentGourbin](https://github.com/VincentGourbin)

---

**Made with ❤️ using Gradio, Qwen3, and Mermaid.js**
