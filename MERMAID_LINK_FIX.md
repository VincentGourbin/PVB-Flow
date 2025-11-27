# Fix: Bouton MermaidChart - Affichage du lien au lieu d'ouverture automatique

## Problème rencontré

Le bouton "Open in Mermaid Chart" ne fonctionnait pas à cause d'un problème de passage de données entre Python et JavaScript dans Gradio :
- Python générait correctement l'URL (921 caractères)
- JavaScript recevait une string vide (0 caractères)

### Logs du problème

**Python (OK):**
```
[DEBUG] Generated URL length: 921
[DEBUG] Generated URL preview: https://www.mermaidchart.com/play?utm_source=...
```

**JavaScript (KO):**
```javascript
[DEBUG] Received URL:
[DEBUG] URL type: string
[DEBUG] URL length: 0
```

## Solution implémentée

Au lieu d'essayer d'ouvrir automatiquement l'URL en JavaScript, on affiche maintenant le lien directement dans l'interface, comme dans l'exemple Claude Desktop.

### Changements effectués

1. **UI (`app.py`):**
   - Bouton renommé : "🔗 Generate MermaidChart Link"
   - Ajout d'une zone `mermaid_url_display` (Markdown) pour afficher le lien
   - Suppression du JavaScript `.then()` qui ne fonctionnait pas

2. **Handler (`handlers.py`):**
   - `handle_open_mermaid_chart()` retourne maintenant un Markdown formaté
   - Le Markdown inclut :
     - Un lien cliquable vers MermaidChart.com
     - L'URL en texte pour copier/coller
     - Instructions d'utilisation

3. **Clear handler:**
   - Ajout d'un output supplémentaire pour réinitialiser l'affichage de l'URL

## Nouveau workflow

1. **Utilisateur génère un diagramme** → Diagramme apparaît dans le preview
2. **Utilisateur clique sur "🔗 Generate MermaidChart Link"** → URL s'affiche en dessous
3. **Utilisateur clique sur le lien** → Nouvel onglet s'ouvre avec MermaidChart.com playground

## Exemple d'affichage

Quand l'utilisateur clique sur le bouton, il voit :

```markdown
### 🔗 Lien MermaidChart Playground

[👉 Cliquez ici pour ouvrir votre diagramme dans MermaidChart.com](https://www.mermaidchart.com/play?utm_source=pvb_flow&utm_medium=gradio_app#pako:eNqdVN1u2jAY...)

Ou copiez le lien ci-dessous :
```
https://www.mermaidchart.com/play?utm_source=pvb_flow&utm_medium=gradio_app#pako:eNqdVN1u2jAY...
```

**Ce que vous pouvez faire sur MermaidChart.com :**
- ✏️ Éditer le diagramme en temps réel
- 📥 Exporter en PNG, SVG, ou PDF
- 🔗 Partager avec votre équipe
- 💾 Sauvegarder dans votre compte (si connecté)
```

## Avantages de cette approche

✅ **Fonctionne de manière fiable** : Pas de problème de passage de données Gradio
✅ **Plus de contrôle pour l'utilisateur** : Peut copier l'URL pour la partager
✅ **Meilleure UX** : Instructions claires, lien visible et cliquable
✅ **Compatible avec tous les navigateurs** : Pas de dépendance au JavaScript
✅ **Similaire à l'exemple Claude Desktop** : Expérience utilisateur cohérente

## Tests

```bash
# Test 1 : Avec un diagramme
python -c "
from src.pvb_flow.ui.handlers import handle_open_mermaid_chart
result = handle_open_mermaid_chart('flowchart TD\n    A[Start] --> B[End]')
print(result)
"

# Test 2 : Sans diagramme
python -c "
from src.pvb_flow.ui.handlers import handle_open_mermaid_chart
result = handle_open_mermaid_chart('')
print(result)
"
```

## Notes

- Le warning Mistral tokenizer a aussi été corrigé avec `fix_mistral_regex=True`
- Les logs de debug sont conservés pour faciliter le débogage futur
