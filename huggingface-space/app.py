#!/usr/bin/env python3
"""
PVB Flow - Hugging Face Spaces Version
Product Vision Board to Mermaid diagram generation with Mistral API.
"""

import gradio as gr
import os
from pathlib import Path

# Import custom modules
from src.ui.spaces_interface import create_spaces_interface

def main():
    """Main entry point for the Hugging Face Spaces app."""

    # Create the Gradio interface
    interface = create_spaces_interface()

    # Launch with specific settings for HF Spaces
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7860))
    interface.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
