# 🚀 Quick Start - Déploiement sur Hugging Face Spaces

## En 2 étapes (pas besoin d'API key!)

### 1️⃣ Obtenir le token Hugging Face

```bash
# Token Hugging Face (avec permissions 'write')
# → https://huggingface.co/settings/tokens
```

### 2️⃣ Déployer

```bash
export HF_TOKEN="hf_xxxxxxxxxxxxx"
cd huggingface-space
pip install huggingface_hub
python3 deploy.py
```

## ✅ C'est fait!

Votre app sera disponible sur :
```
https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator
```

## 🧪 Tester en local d'abord

⚠️ **Note**: Le test local nécessite une carte graphique NVIDIA avec CUDA
(ZeroGPU n'est pas disponible en local)

```bash
cd huggingface-space
pip install -r requirements.txt
python3 test_local.py
```

Ouvrir : http://localhost:7860

Ou déployer directement sur HF Spaces pour utiliser ZeroGPU!

---

📖 **Documentation complète** : Voir [DEPLOYMENT.md](./DEPLOYMENT.md)
