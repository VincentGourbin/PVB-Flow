# 🚀 Déploiement sur Hugging Face Spaces

Guide complet pour déployer PVB Flow sur Hugging Face Spaces.

## 📋 Prérequis

1. **Compte Hugging Face**
   - Créer un compte sur https://huggingface.co/
   - Obtenir un token avec permissions `write` : https://huggingface.co/settings/tokens

2. **Clé API Mistral**
   - Créer un compte sur https://console.mistral.ai/
   - Obtenir une clé API Mistral

3. **Dépendances Python**
   ```bash
   pip install huggingface_hub
   ```

## 🎯 Méthode 1: Déploiement automatique (Recommandé)

### 1. Configurer les variables d'environnement

```bash
# Token Hugging Face
export HF_TOKEN="votre_token_huggingface"

# Clé API Mistral (optionnel pour auto-config)
export MISTRAL_API_KEY="votre_cle_api_mistral"
```

### 2. Exécuter le script de déploiement

```bash
cd huggingface-space
python3 deploy.py
```

Le script va :
- ✅ Vérifier les dépendances
- ✅ Créer le Space sur Hugging Face (ou le mettre à jour s'il existe)
- ✅ Uploader tous les fichiers nécessaires
- ✅ Configurer les secrets (MISTRAL_API_KEY)
- ✅ Lancer le build

### 3. Configurer les secrets manuellement (si nécessaire)

Si `MISTRAL_API_KEY` n'est pas dans l'environnement :

1. Aller sur : `https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator/settings`
2. Aller dans la section "Repository secrets"
3. Ajouter le secret :
   - **Name**: `MISTRAL_API_KEY`
   - **Value**: Votre clé API Mistral

### 4. Vérifier le déploiement

- URL du Space : `https://huggingface.co/spaces/VincentGOURBIN/PVB-Flow-Mermaid-Generator`
- Attendre que le build se termine (1-3 minutes)
- Tester l'application

## 🛠️ Méthode 2: Déploiement manuel

### 1. Créer le Space sur Hugging Face

1. Aller sur https://huggingface.co/new-space
2. Configurer :
   - **Owner**: Votre username
   - **Space name**: `PVB-Flow-Mermaid-Generator`
   - **SDK**: Gradio
   - **Hardware**: CPU (gratuit)
   - **Visibility**: Public

### 2. Cloner le repo du Space

```bash
git clone https://huggingface.co/spaces/VOTRE_USERNAME/PVB-Flow-Mermaid-Generator
cd PVB-Flow-Mermaid-Generator
```

### 3. Copier les fichiers

```bash
# Depuis le dossier huggingface-space
cp app.py PVB-Flow-Mermaid-Generator/
cp requirements.txt PVB-Flow-Mermaid-Generator/
cp README.md PVB-Flow-Mermaid-Generator/
cp -r src/ PVB-Flow-Mermaid-Generator/
```

### 4. Commit et push

```bash
cd PVB-Flow-Mermaid-Generator
git add .
git commit -m "Initial deployment"
git push
```

### 5. Configurer les secrets

Comme dans la méthode 1, étape 3.

## 🧪 Test en local avant déploiement

Pour tester localement avec la configuration Spaces :

```bash
# Depuis le dossier huggingface-space

# 1. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
export MISTRAL_API_KEY="votre_cle_api_mistral"

# 4. Lancer l'app
python3 app.py
```

Ouvrir : `http://localhost:7860`

## 🔧 Configuration du Space

### Métadonnées (dans README.md)

```yaml
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
---
```

### Hardware

- **CPU** : Gratuit, suffisant pour l'API Mistral (pas de modèle local)
- **GPU** : Non nécessaire (on utilise l'API)

### Secrets requis

| Nom | Description | Requis |
|-----|-------------|---------|
| `MISTRAL_API_KEY` | Clé API Mistral | ✅ Oui |

## 📊 Structure des fichiers déployés

```
PVB-Flow-Mermaid-Generator/
├── app.py                    # Point d'entrée Gradio
├── requirements.txt          # Dépendances Python
├── README.md                 # Métadonnées + Documentation
└── src/
    ├── __init__.py
    ├── ai/
    │   ├── __init__.py
    │   ├── mistral_api_analyzer.py  # Client API Mistral
    │   └── prompts_config.py        # Prompts système
    ├── ui/
    │   ├── __init__.py
    │   └── spaces_interface.py      # Interface Gradio
    ├── utils/
    │   ├── __init__.py
    │   └── json_validator.py        # Validation JSON PVB
    └── core/
        ├── __init__.py
        ├── mermaid_encoder.py       # Encodage URLs Mermaid
        └── mermaid_extractor.py     # Extraction code Mermaid
```

## 🐛 Dépannage

### Erreur: "Mistral API not configured"

**Problème** : La clé API Mistral n'est pas configurée.

**Solution** :
1. Vérifier que le secret `MISTRAL_API_KEY` est bien configuré dans les settings du Space
2. Redémarrer le Space (Factory reboot)

### Erreur: "ModuleNotFoundError"

**Problème** : Dépendances manquantes.

**Solution** :
1. Vérifier que `requirements.txt` contient toutes les dépendances
2. Forcer un rebuild du Space

### Le Space ne démarre pas

**Problème** : Erreur dans le code ou les dépendances.

**Solution** :
1. Consulter les logs du Space dans l'interface HF
2. Tester en local d'abord avec `python3 app.py`
3. Vérifier la structure des fichiers

## 🔄 Mise à jour du Space

### Avec le script de déploiement

```bash
cd huggingface-space
python3 deploy.py
```

Le script détecte automatiquement si le Space existe et le met à jour.

### Manuellement

```bash
cd PVB-Flow-Mermaid-Generator
git add .
git commit -m "Update: votre message"
git push
```

## 📝 Personnalisation

### Changer le nom du Space

Modifier dans `deploy.py` :

```python
SPACE_NAME = "VotreUsername/Nom-Du-Space"
```

### Changer le modèle Mistral

Modifier dans `src/ai/mistral_api_analyzer.py` :

```python
model_name: str = "mistral-large-latest"  # ou mistral-small-latest
```

### Ajouter des fonctionnalités

1. Modifier les fichiers dans `src/`
2. Tester en local
3. Redéployer avec `python3 deploy.py`

## 📚 Ressources

- **Hugging Face Spaces** : https://huggingface.co/docs/hub/spaces
- **Gradio v6** : https://gradio.app/docs
- **Mistral API** : https://docs.mistral.ai/
- **Mermaid Live Editor** : https://mermaid.live/

## ✅ Checklist de déploiement

Avant de déployer, vérifier :

- [ ] Token HuggingFace avec permissions `write`
- [ ] Clé API Mistral valide
- [ ] Tous les fichiers présents dans `huggingface-space/`
- [ ] Tests locaux passés
- [ ] README.md avec métadonnées correctes
- [ ] requirements.txt à jour
- [ ] Script `deploy.py` configuré avec le bon SPACE_NAME

---

🎉 **Bon déploiement !**
