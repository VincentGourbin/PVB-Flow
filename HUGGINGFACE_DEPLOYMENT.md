# 🚀 Déploiement Hugging Face Spaces - PVB Flow

Ce document explique comment déployer PVB Flow sur Hugging Face Spaces.

## 📁 Localisation

Tous les fichiers pour Hugging Face Spaces sont dans le dossier :
```
/huggingface-space/
```

## 🎯 Vue d'ensemble

Le projet a maintenant **deux versions** :

### Version 1: Locale (MLX) - Dossier principal
- **Fichier** : `main.py`
- **Backend** : MLX (Apple Silicon uniquement)
- **Modèles** : Locaux, quantized 8-bit
- **Usage** : Développement local sur Mac M1/M2/M3

### Version 2: Hugging Face Spaces - Dossier `/huggingface-space/`
- **Fichier** : `app.py`
- **Backend** : API Mistral (cloud)
- **Modèles** : Via API Mistral
- **Usage** : Déploiement public sur HF Spaces

## 🚀 Déploiement rapide

### Prérequis

1. **Token Hugging Face** avec permissions `write`
   - Obtenir sur : https://huggingface.co/settings/tokens

2. **Clé API Mistral**
   - Obtenir sur : https://console.mistral.ai/

### Commandes

```bash
# 1. Aller dans le dossier Hugging Face Spaces
cd huggingface-space

# 2. Configurer les tokens
export HF_TOKEN="votre_token_huggingface"
export MISTRAL_API_KEY="votre_cle_mistral"

# 3. Installer les dépendances de déploiement
pip install huggingface_hub

# 4. Déployer
python3 deploy.py
```

Le script `deploy.py` :
- ✅ Crée automatiquement le Space sur HuggingFace
- ✅ Upload tous les fichiers nécessaires
- ✅ Configure les secrets (MISTRAL_API_KEY)
- ✅ Lance le build du Space

### URL du Space déployé

Après déploiement, votre app sera disponible sur :
```
https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator
```

## 📊 Architecture

### Fichiers déployés sur HF Spaces

```
huggingface-space/
├── app.py                      # Entry point Gradio
├── requirements.txt            # Dépendances cloud (API seulement)
├── README.md                   # Métadonnées HF + Documentation
└── src/
    ├── ai/
    │   ├── mistral_api_analyzer.py    # Client API Mistral
    │   └── prompts_config.py          # Prompts système
    ├── ui/
    │   └── spaces_interface.py        # Interface Gradio
    ├── utils/
    │   └── json_validator.py          # Validation PVB JSON
    └── core/
        ├── mermaid_encoder.py         # Encodage URLs Mermaid Live
        └── mermaid_extractor.py       # Extraction code Mermaid
```

### Fichiers de configuration (locaux uniquement)

```
huggingface-space/
├── deploy.py                   # Script de déploiement auto
├── test_local.py               # Test local avant déploiement
├── DEPLOYMENT.md               # Guide de déploiement détaillé
├── LOCAL_README.md             # Documentation développeur
├── .env.example                # Exemple de configuration
└── .gitignore                  # Fichiers à ignorer
```

## 🧪 Test en local

Avant de déployer, tester localement :

```bash
cd huggingface-space

# Configurer la clé API
export MISTRAL_API_KEY="votre_cle"

# Installer les dépendances
pip install -r requirements.txt

# Tester
python3 test_local.py
```

Ouvrir : http://localhost:7860

## 🔧 Configuration

### Secrets Hugging Face Spaces

Après déploiement, vérifier que le secret est configuré :

1. Aller sur : https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator/settings
2. Section "Repository secrets"
3. Vérifier que `MISTRAL_API_KEY` est bien configuré

### Personnalisation

#### Changer le nom du Space

Éditer `huggingface-space/deploy.py` :

```python
SPACE_NAME = "VotreUsername/Nom-Du-Space"
```

#### Changer le modèle Mistral

Éditer `huggingface-space/src/ai/mistral_api_analyzer.py` :

```python
model_name: str = "mistral-large-latest"  # ou mistral-small-latest
```

## 📚 Documentation

- **Guide de déploiement complet** : [`huggingface-space/DEPLOYMENT.md`](./huggingface-space/DEPLOYMENT.md)
- **Documentation développeur** : [`huggingface-space/LOCAL_README.md`](./huggingface-space/LOCAL_README.md)
- **Documentation utilisateur** : [`huggingface-space/README.md`](./huggingface-space/README.md)

## 🔄 Mise à jour du Space

Pour mettre à jour le Space après modifications :

```bash
cd huggingface-space
python3 deploy.py
```

Le script détecte automatiquement que le Space existe et le met à jour.

## 🆚 Comparaison des versions

| Aspect | Version locale | Version Spaces |
|--------|---------------|----------------|
| **Déploiement** | `python main.py` | `python deploy.py` |
| **Backend ML** | MLX (Apple Silicon) | Mistral API |
| **Modèles** | Local (8-bit quantized) | Cloud (API) |
| **Hardware** | M1/M2/M3 Mac requis | N'importe quel CPU |
| **Coût** | Gratuit | Pay-per-use |
| **Latence** | Très rapide (local) | Dépend de l'API |
| **Dépendances** | mlx_lm, torch | mistralai, gradio |
| **Accès** | Local uniquement | Public (internet) |

## ✅ Checklist de déploiement

Avant de déployer :

- [ ] Token HuggingFace avec permissions `write` obtenu
- [ ] Clé API Mistral obtenue et testée
- [ ] Tests locaux passés (`python3 test_local.py`)
- [ ] Fichiers vérifiés dans `huggingface-space/`
- [ ] Variables d'environnement configurées
- [ ] Script `deploy.py` configuré avec le bon SPACE_NAME

Après déploiement :

- [ ] Space créé sur HuggingFace
- [ ] Build terminé avec succès
- [ ] Secret `MISTRAL_API_KEY` configuré
- [ ] App testée en ligne
- [ ] Génération de diagrammes fonctionnelle
- [ ] Liens Mermaid Live Editor fonctionnels

## 🐛 Dépannage

### Le déploiement échoue

1. Vérifier les tokens/clés API
2. Tester en local d'abord
3. Consulter les logs dans le terminal

### Le Space ne démarre pas

1. Vérifier les logs dans l'interface HF Spaces
2. Vérifier que `MISTRAL_API_KEY` est configuré dans les secrets
3. Factory reboot du Space

### "Mistral API not configured"

- Secret `MISTRAL_API_KEY` manquant dans les settings du Space
- Ajouter manuellement dans les Repository secrets

## 🔗 Liens utiles

- **Hugging Face Spaces** : https://huggingface.co/docs/hub/spaces
- **Obtenir token HF** : https://huggingface.co/settings/tokens
- **Obtenir clé Mistral** : https://console.mistral.ai/
- **Gradio v6** : https://gradio.app/docs
- **Mistral API** : https://docs.mistral.ai/

---

🎉 **Prêt pour le déploiement !**

Pour plus de détails, consultez [`huggingface-space/DEPLOYMENT.md`](./huggingface-space/DEPLOYMENT.md)
