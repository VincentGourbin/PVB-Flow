# Instructions de Débogage - Bouton MermaidChart

## Problème

Le bouton "🔗 Open in Mermaid Chart" affiche une erreur "No diagram to share" alors qu'un diagramme est visible dans le preview.

## Étapes de Débogage

### 1. Lance l'application avec les logs

```bash
cd /Users/vincent/Developpements/AppAutomatedProcess
python main.py
```

### 2. Génère un diagramme

1. Colle ton Product Vision Board JSON dans le chat
2. Attends que le diagramme apparaisse dans le preview à droite
3. **Vérifie dans le terminal** - tu devrais voir :
   ```
   [DEBUG] Mermaid extraction - is_valid: True, code_length: XXX
   [DEBUG] Updated current_diagram with XXX characters
   [DEBUG] current_diagram to be returned: XXX chars
   ```

### 3. Clique sur "🔗 Open in Mermaid Chart"

**Dans le terminal**, tu devrais voir :
```
[DEBUG] handle_open_mermaid_chart called
[DEBUG] current_diagram type: <class 'str'>
[DEBUG] current_diagram length: XXX
[DEBUG] current_diagram preview: flowchart TD...
[DEBUG] Generated URL length: XXX
[DEBUG] Generated URL preview: https://www.mermaidchart.com/play...
```

**Dans la console du navigateur** (F12 → Console), tu devrais voir :
```
[DEBUG] JS handler called with URL: https://www.mermaidchart.com/play...
[DEBUG] URL type: string
[DEBUG] URL length: XXX
[DEBUG] Opening URL in new tab
```

## Diagnostic selon les logs

### Cas 1 : "current_diagram length: 0" dans le terminal
**Problème** : Le state `diagram_state` n'est pas mis à jour
**Solution** : Le problème est dans le mapping des outputs de `handle_message`

### Cas 2 : "Generated URL length: 0" dans le terminal
**Problème** : L'encodage du diagramme échoue
**Solution** : Vérifier `mermaid_encoder.py`

### Cas 3 : "URL type: undefined" ou "URL length: 0" dans la console navigateur
**Problème** : Le state n'est pas passé au JavaScript
**Solution** : Le problème est dans le flow `.then()` de Gradio

### Cas 4 : Aucun log "[DEBUG] handle_open_mermaid_chart called"
**Problème** : Le handler Python n'est jamais appelé
**Solution** : Le bouton n'est pas correctement lié

## À me communiquer

Copie-colle :
1. **Tous les logs du terminal** depuis le moment où tu génères le diagramme jusqu'à l'erreur
2. **Les logs de la console navigateur** (F12 → Console) quand tu cliques sur le bouton
3. **Une capture d'écran** de l'erreur qui apparaît

## Workaround temporaire

Si ça ne fonctionne toujours pas, on peut essayer une approche alternative :
- Afficher l'URL en texte dans l'interface
- L'utilisateur copie l'URL manuellement
- On corrige le problème du bouton ensuite
