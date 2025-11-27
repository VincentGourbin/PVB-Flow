# 📊 PVB Flow - Hugging Face Spaces Version

Version de PVB Flow optimisée pour Hugging Face Spaces avec API Mistral.

## 🎯 Différences avec la version locale

| Fonctionnalité | Version locale (main.py) | Version Spaces |
|----------------|-------------------------|----------------|
| **Backend ML** | MLX (Apple Silicon) | API Mistral |
| **Modèles** | Local (quantized 8-bit) | Cloud (Mistral API) |
| **Hardware** | M1/M2/M3 Mac requis | N'importe quel CPU |
| **Déploiement** | Local uniquement | Cloud public |
| **Coût** | Gratuit (local) | Pay-per-use (API) |

## 🚀 Quick Start

### 1. Test en local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API Mistral
export MISTRAL_API_KEY="votre_cle_api"

# Tester l'app
python3 test_local.py
```

Ouvrir : http://localhost:7860

### 2. Déployer sur Hugging Face Spaces

```bash
# Configurer le token HuggingFace
export HF_TOKEN="votre_token_hf"

# Optionnel: configurer Mistral API pour auto-setup
export MISTRAL_API_KEY="votre_cle_mistral"

# Déployer
python3 deploy.py
```

📖 **Documentation complète** : Voir [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 Structure du projet

```
huggingface-space/
├── app.py                    # Point d'entrée Gradio
├── requirements.txt          # Dépendances (API uniquement)
├── README.md                 # Métadonnées HF + Doc utilisateur
├── DEPLOYMENT.md             # Guide de déploiement complet
├── deploy.py                 # Script de déploiement automatique
├── test_local.py             # Script de test local
├── .env.example              # Exemple de configuration
├── .gitignore                # Fichiers à ignorer
└── src/
    ├── ai/
    │   ├── mistral_api_analyzer.py    # Client API Mistral
    │   └── prompts_config.py          # Prompts (copié)
    ├── ui/
    │   └── spaces_interface.py        # Interface Gradio adaptée
    ├── utils/
    │   └── json_validator.py          # Validation (copié)
    └── core/
        ├── mermaid_encoder.py         # Encodage URLs (copié)
        └── mermaid_extractor.py       # Extraction (copié)
```

## 🔑 Configuration requise

### Pour tester en local

```bash
# .env (ne pas committer)
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Pour déployer sur HF Spaces

1. **Token HuggingFace** (variable d'environnement ou interactif)
   ```bash
   export HF_TOKEN="hf_xxxxxxxxxxxxx"
   ```

2. **Secret du Space** (configuré automatiquement par deploy.py ou manuellement)
   - Nom: `MISTRAL_API_KEY`
   - Valeur: Votre clé API Mistral

## 🧪 Tests avant déploiement

### 1. Vérifier l'environnement

```bash
python3 test_local.py
```

Cela vérifie :
- ✅ Version Python (3.8+)
- ✅ Clé API Mistral configurée
- ✅ Dépendances installées
- ✅ Lance l'app en local

### 2. Tester manuellement

```bash
# 1. Lancer l'app
python3 app.py

# 2. Ouvrir dans le navigateur
open http://localhost:7860

# 3. Tester avec un PVB JSON (voir README.md pour un exemple)
```

## 📊 Utilisation

### Exemple de Product Vision Board JSON

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

### Workflow

1. **Coller le JSON** dans le chat
2. **Attendre la génération** du diagramme (côté droit)
3. **Raffiner** en chattant :
   - "make it more vertical"
   - "add more colors"
   - "simplify the diagram"
4. **Générer un lien** Mermaid Live Editor pour partager

## 🔧 Personnalisation

### Changer le modèle Mistral

Éditer `src/ai/mistral_api_analyzer.py` :

```python
def __init__(
    self,
    api_key: str = None,
    model_name: str = "mistral-large-latest"  # ou mistral-small-latest
):
```

### Modifier les prompts

Éditer `src/ai/prompts_config.py` pour personnaliser :
- Le prompt système
- Les instructions de génération
- Le format des diagrammes

### Changer le nom/URL du Space

Éditer `deploy.py` :

```python
SPACE_NAME = "VotreUsername/Nom-Du-Space"
SPACE_TITLE = "Votre Titre"
```

## 🐛 Dépannage

### "Mistral API not configured"

```bash
# Vérifier que la variable est définie
echo $MISTRAL_API_KEY

# Si vide, la définir
export MISTRAL_API_KEY="votre_cle"
```

### "ModuleNotFoundError"

```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Le déploiement échoue

```bash
# Vérifier les logs
python3 deploy.py

# Tester d'abord en local
python3 test_local.py
```

## 📚 Ressources

- **Documentation de déploiement** : [DEPLOYMENT.md](./DEPLOYMENT.md)
- **README principal** : [README.md](./README.md) (pour HF Spaces)
- **Hugging Face Spaces** : https://huggingface.co/docs/hub/spaces
- **Mistral API** : https://docs.mistral.ai/
- **Gradio v6** : https://gradio.app/docs

## 🔗 Liens utiles

- **Obtenir un token HF** : https://huggingface.co/settings/tokens
- **Obtenir une clé Mistral** : https://console.mistral.ai/
- **Mermaid Live Editor** : https://mermaid.live/

---

🎉 **Ready to deploy!**
