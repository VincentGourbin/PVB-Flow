"""
Gradio v6 interface for Hugging Face Spaces.
Uses Mistral API for diagram generation.
"""
import gradio as gr
import os
from typing import Tuple, List, Dict
from ..ai.qwen_zerogpu_analyzer import QwenZeroGPUAnalyzer
from ..ai.prompts_config import DiagramPrompts
from ..utils.json_validator import validate_pvb_json
from ..core.mermaid_extractor import extract_mermaid_code
from ..core.mermaid_encoder import generate_mermaid_chart_url


def create_spaces_interface():
    """
    Create Gradio interface for Hugging Face Spaces.

    Returns:
        Gradio Blocks demo
    """

    # Initialize Qwen ZeroGPU analyzer
    try:
        analyzer = QwenZeroGPUAnalyzer()
        print("✅ Qwen ZeroGPU analyzer initialized")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize Qwen analyzer: {e}")
        analyzer = None

    def handle_message(
        user_input: str,
        conversation: List[Dict[str, str]],
        current_diagram: str,
        pvb_data: Dict
    ) -> Tuple[List[Dict[str, str]], str, List[Dict], str, Dict, str]:
        """Handle user message and generate response."""

        if not analyzer:
            error_msg = "❌ Model not initialized. Please check the Space logs."
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": error_msg})
            diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "Model not initialized"
            return conversation, diagram_preview, conversation, current_diagram, pvb_data, ""

        if not user_input or not user_input.strip():
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

        # Add display message to conversation
        conversation.append({"role": "user", "content": display_message})

        try:
            # Create LLM conversation with the actual prompt
            llm_conversation = conversation[:-1]  # All messages except the last one
            llm_conversation.append({"role": "user", "content": prompt})

            # Generate response with Qwen ZeroGPU
            response = analyzer.generate_response(llm_conversation)

            # Extract Mermaid code from response
            mermaid_code, is_valid = extract_mermaid_code(response)

            if is_valid and mermaid_code:
                current_diagram = mermaid_code

            # Format diagram preview
            diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "No diagram yet..."

            # For chat display: show only text without the Mermaid code block
            import re
            chat_response = re.sub(r'```mermaid\n.*?\n```', '', response, flags=re.DOTALL).strip()

            if not chat_response:
                chat_response = "Diagramme généré avec succès ! Consultez le panneau de droite pour visualiser le résultat."

            conversation.append({"role": "assistant", "content": chat_response})

        except Exception as e:
            error_message = f"Error generating response: {str(e)}"
            conversation.append({"role": "assistant", "content": error_message})
            diagram_preview = f"```mermaid\n{current_diagram}\n```" if current_diagram else "Error occurred"

        return (
            conversation,
            diagram_preview,
            conversation,
            current_diagram,
            pvb_data,
            ""
        )

    def handle_clear() -> Tuple[List, str, List, str, Dict, str]:
        """Clear all conversation and state."""
        return (
            [],
            "Diagram will appear here...",
            [],
            "",
            {},
            ""
        )

    def handle_generate_link(diagram_preview: str) -> str:
        """Generate Mermaid Live Editor link."""
        import time
        import hashlib
        import re

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Extract Mermaid code from preview
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        match = re.search(mermaid_pattern, diagram_preview, re.DOTALL)

        if not match:
            return "⚠️ **Pas de diagramme à partager.** Veuillez d'abord générer un diagramme."

        current_diagram = match.group(1).strip()

        if not current_diagram or not current_diagram.strip():
            return "⚠️ **Pas de diagramme à partager.** Veuillez d'abord générer un diagramme."

        # Generate hash for verification
        diagram_hash = hashlib.md5(current_diagram.encode()).hexdigest()[:8]

        url = generate_mermaid_chart_url(current_diagram)

        if url:
            first_line = current_diagram.split('\n')[0] if current_diagram else 'N/A'

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

    # Build Gradio interface
    with gr.Blocks(title="Product Vision Board → Mermaid Diagram") as demo:
        # Header
        gr.Markdown(
            """
            # 📊 Product Vision Board → Mermaid Diagram Generator
            **Transform your Product Vision Board into professional Mermaid flowcharts**
            """
        )

        # Instructions
        with gr.Accordion("📖 How to use", open=False):
            gr.Markdown(
                """
                ### Getting Started

                1. **Paste your Product Vision Board JSON** in the chat input (see example below)
                2. **Wait for the diagram** to be generated
                3. **Refine the diagram** by chatting (e.g., "make it more vertical", "add more colors", "simplify")

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

                ### Tips
                - The chatbot will auto-render Mermaid diagrams
                - You can request layout changes (vertical/horizontal)
                - Ask for visual enhancements (colors, icons, subgraphs)
                - Iterate until you're happy with the result!
                """
            )

        # Main content: Two-column layout
        with gr.Row():
            # LEFT COLUMN: Chatbot
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    value=[],
                    height=650,
                    label="Conversation"
                )

                # Input area
                msg_input = gr.Textbox(
                    placeholder="Paste your Product Vision Board JSON or ask for diagram refinements...",
                    lines=5,
                    show_label=False,
                    max_lines=10
                )

                # Action buttons
                with gr.Row():
                    send_btn = gr.Button("📤 Send", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")

            # RIGHT COLUMN: Diagram Preview
            with gr.Column(scale=1):
                gr.Markdown("### 📈 Diagram Preview")
                diagram_preview = gr.Markdown(
                    value="*Paste your Product Vision Board JSON to generate a diagram...*",
                    height=500
                )

                # Diagram actions
                with gr.Row():
                    open_chart_btn = gr.Button("🔗 Generate Mermaid Live Link", variant="primary")

                # URL display area
                mermaid_url_display = gr.Markdown(
                    value="",
                    label="Mermaid Live Editor Link"
                )

                gr.Markdown("*Click the button to generate a shareable link. Then click the link to open in Mermaid Live Editor!*")

        # State management
        conversation_state = gr.State([])
        diagram_state = gr.State("")
        pvb_state = gr.State({})

        # Event handlers
        send_btn.click(
            fn=handle_message,
            inputs=[msg_input, conversation_state, diagram_state, pvb_state],
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, msg_input]
        )

        msg_input.submit(
            fn=handle_message,
            inputs=[msg_input, conversation_state, diagram_state, pvb_state],
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, msg_input]
        )

        clear_btn.click(
            fn=handle_clear,
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, mermaid_url_display]
        )

        open_chart_btn.click(
            fn=handle_generate_link,
            inputs=[diagram_preview],
            outputs=[mermaid_url_display]
        )

        # Footer
        gr.Markdown(
            """
            ---
            Made with ❤️ using [Gradio v6](https://gradio.app) • Powered by Qwen3-4B-Instruct with ZeroGPU
            """
        )

    return demo
