"""
Gradio v6 interface for Product Vision Board to Mermaid diagram generation.
"""
import gradio as gr
from .handlers import handle_message, handle_clear, handle_open_mermaid_chart


def create_ui(analyzer):
    """
    Create the Gradio interface.

    Args:
        analyzer: LLM analyzer instance (MistralMLXAnalyzer or MistralTextAnalyzer)

    Returns:
        Gradio Blocks demo
    """
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

        # Event handlers - explicitly update all states
        def send_message_wrapper(*args):
            result = handle_message(*args)
            print(f"[DEBUG] send_message_wrapper output diagram_state index 3 length: {len(result[3]) if result[3] else 0}")
            return result

        send_event = send_btn.click(
            fn=send_message_wrapper,
            inputs=[msg_input, conversation_state, diagram_state, pvb_state, gr.State(analyzer)],
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, msg_input]
        )

        # Also trigger on Enter key
        msg_input.submit(
            fn=send_message_wrapper,
            inputs=[msg_input, conversation_state, diagram_state, pvb_state, gr.State(analyzer)],
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, msg_input]
        )

        # Clear button
        clear_btn.click(
            fn=handle_clear,
            outputs=[chatbot, diagram_preview, conversation_state, diagram_state, pvb_state, mermaid_url_display]
        )

        # Generate MermaidChart link button
        # NEW: Read from diagram_preview instead of diagram_state (fixes stale state issue)
        open_chart_btn.click(
            fn=handle_open_mermaid_chart,
            inputs=[diagram_preview],  # Changed from diagram_state to diagram_preview
            outputs=[mermaid_url_display]
        )

        # Footer
        gr.Markdown(
            """
            ---
            Made with ❤️ using [Gradio v6](https://gradio.app) • Powered by Mistral AI
            """
        )

    return demo
