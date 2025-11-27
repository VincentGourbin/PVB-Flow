"""
Event handlers for Gradio UI interactions.
"""
from typing import Tuple, List, Dict, Any
from ..utils.json_validator import validate_pvb_json
from ..ai.prompts_config import DiagramPrompts
from ..core.mermaid_extractor import extract_mermaid_code, format_for_display
from ..core.mermaid_encoder import generate_mermaid_chart_url


def handle_message(
    user_input: str,
    conversation: List[Dict[str, str]],
    current_diagram: str,
    pvb_data: Dict,
    analyzer: Any
) -> Tuple[List[Dict[str, str]], str, List[Dict], str, Dict, str]:
    """
    Handle user message and generate response.

    Args:
        user_input: User's input message
        conversation: Conversation history (for LLM and display)
        current_diagram: Current Mermaid diagram code
        pvb_data: Product Vision Board data
        analyzer: LLM analyzer instance

    Returns:
        Tuple of (chatbot_history, diagram_preview, conversation, current_diagram, pvb_data, cleared_input)
    """
    if not user_input or not user_input.strip():
        # Empty input, return current state
        diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "Diagram will appear here..."
        return conversation, diagram_preview, conversation, current_diagram, pvb_data, ""

    # Check if this is initial PVB input or refinement
    if not pvb_data:
        # Try to parse as PVB JSON
        is_valid, parsed_pvb, error = validate_pvb_json(user_input)

        if is_valid:
            # Valid PVB JSON - generate initial diagram
            pvb_data = parsed_pvb
            prompt = DiagramPrompts.get_initial_prompt(pvb_data)
            display_message = "Here's my Product Vision Board. Please generate a Mermaid diagram."
        else:
            # Not valid PVB JSON, treat as regular message
            prompt = user_input
            display_message = user_input
    else:
        # Refinement request
        prompt = DiagramPrompts.get_refinement_prompt(pvb_data, current_diagram, user_input)
        display_message = user_input

    # Add display message to conversation (what user sees)
    conversation.append({"role": "user", "content": display_message})

    try:
        # Create LLM conversation with the actual prompt
        llm_conversation = conversation[:-1]  # All messages except the last one
        llm_conversation.append({"role": "user", "content": prompt})

        # Generate response with LLM
        response = analyzer.generate_response(llm_conversation)

        # Extract Mermaid code from response
        mermaid_code, is_valid = extract_mermaid_code(response)

        print(f"[DEBUG] Mermaid extraction - is_valid: {is_valid}, code_length: {len(mermaid_code) if mermaid_code else 0}")

        if is_valid and mermaid_code:
            # Update current diagram
            current_diagram = mermaid_code
            print(f"[DEBUG] Updated current_diagram with {len(current_diagram)} characters")

        # Format diagram preview
        diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "No diagram yet..."
        print(f"[DEBUG] current_diagram to be returned: {len(current_diagram) if current_diagram else 0} chars")

        # For chat display: show only text without the Mermaid code block
        # Extract text before and after the mermaid block
        import re
        chat_response = re.sub(r'```mermaid\n.*?\n```', '', response, flags=re.DOTALL).strip()

        # If no text remains, add a default message
        if not chat_response:
            chat_response = "Diagramme généré avec succès ! Consultez le panneau de droite pour visualiser le résultat."

        # Add cleaned response to conversation (for chat display)
        conversation.append({"role": "assistant", "content": chat_response})

    except Exception as e:
        # Handle errors gracefully
        import traceback
        error_message = f"Error generating response: {str(e)}\n\n{traceback.format_exc()}"
        conversation.append({"role": "assistant", "content": error_message})
        diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "Error occurred"

    print(f"[DEBUG] handle_message returning:")
    print(f"  - current_diagram length: {len(current_diagram) if current_diagram else 0}")
    print(f"  - current_diagram first 100 chars: {current_diagram[:100] if current_diagram else 'EMPTY'}")

    return (
        conversation,          # Chatbot display (same as conversation now)
        diagram_preview,       # Diagram preview
        conversation,          # Updated conversation state
        current_diagram,       # Updated diagram code
        pvb_data,             # PVB data
        ""                    # Clear input field
    )


def format_conversation_for_chatbot(conversation: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Format conversation history for Gradio Chatbot component.
    Gradio v6 expects: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]

    Args:
        conversation: List of {role, content} dictionaries

    Returns:
        List of message dictionaries
    """
    # Gradio v6 uses the same format we already have
    return conversation


def handle_clear() -> Tuple[List, str, List, str, Dict, str]:
    """
    Clear all conversation and state.

    Returns:
        Tuple of empty states for all components
    """
    return (
        [],                           # Empty chatbot history
        "Diagram will appear here...", # Reset diagram preview
        [],                           # Empty conversation
        "",                           # Empty current diagram
        {},                           # Empty PVB data
        ""                            # Clear URL display
    )


def handle_open_mermaid_chart_from_state(current_diagram: str) -> str:
    """ORIGINAL - Read from diagram_state (not working reliably)"""
    return _generate_mermaid_link(current_diagram)


def handle_open_mermaid_chart(diagram_preview: str) -> str:
    """
    Generate MermaidChart.com playground URL for the current diagram.

    NEW APPROACH: Read from diagram_preview (Markdown) instead of diagram_state.

    Args:
        diagram_preview: The Markdown content from the preview pane (contains ```mermaid...```)

    Returns:
        Formatted Markdown with clickable link to MermaidChart.com playground
    """
    import time
    import hashlib
    import re

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*80)
    print(f"[DEBUG] handle_open_mermaid_chart called at {timestamp}")
    print(f"[DEBUG] diagram_preview type: {type(diagram_preview)}")
    print(f"[DEBUG] diagram_preview length: {len(diagram_preview) if diagram_preview else 0}")
    print(f"[DEBUG] diagram_preview RAW:")
    print("-"*80)
    print(diagram_preview if diagram_preview else 'EMPTY')
    print("-"*80)

    # Extract Mermaid code from the preview markdown
    # Preview format is: ```mermaid\n<code>\n```
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    match = re.search(mermaid_pattern, diagram_preview, re.DOTALL)

    if not match:
        print("[DEBUG] No mermaid code found in preview")
        print("="*80 + "\n")
        return "⚠️ **Pas de diagramme à partager.** Veuillez d'abord générer un diagramme."

    current_diagram = match.group(1).strip()
    print(f"[DEBUG] Extracted diagram length: {len(current_diagram)}")
    print(f"[DEBUG] Extracted diagram preview:")
    print(current_diagram[:200] if len(current_diagram) > 200 else current_diagram)

    if not current_diagram or not current_diagram.strip():
        print("[DEBUG] Extracted diagram is empty")
        print("="*80 + "\n")
        return "⚠️ **Pas de diagramme à partager.** Veuillez d'abord générer un diagramme."

    # Generate hash for verification
    diagram_hash = hashlib.md5(current_diagram.encode()).hexdigest()[:8]

    url = generate_mermaid_chart_url(current_diagram)
    print(f"[DEBUG] Generated URL length: {len(url) if url else 0}")
    print(f"[DEBUG] Diagram hash: {diagram_hash}")
    print(f"[DEBUG] Generated URL FULL:")
    print(url)
    print("="*80 + "\n")

    if url:
        # Extract unique identifier from diagram (first line for verification)
        first_line = current_diagram.split('\n')[0] if current_diagram else 'N/A'

        # Return formatted Markdown with clickable link (with timestamp to force refresh)
        return f"""### 🔗 Lien Mermaid Live Editor

**Généré à:** {timestamp} | **Hash:** `{diagram_hash}`
**Diagramme:** `{first_line}` ({len(current_diagram)} caractères)

[**👉 Cliquez ici pour ouvrir votre diagramme dans Mermaid Live Editor**]({url})

Ou copiez le lien ci-dessous :
```
{url}
```

**Ce que vous pouvez faire sur Mermaid Live Editor :**
- ✏️ Éditer le diagramme en temps réel
- 📥 Exporter en PNG, SVG, ou PDF
- 🔗 Partager avec votre équipe
- 💾 Télécharger le code ou l'image
"""
    else:
        return "❌ **Erreur lors de la génération du lien.** Veuillez réessayer."
