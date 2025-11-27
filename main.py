"""
Main entry point for the Product Vision Board to Mermaid Diagram application.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.pvb_flow.ai.analyzer_factory import create_analyzer, print_system_info
from src.pvb_flow.ui.app import create_ui


def main():
    """Main application entry point."""
    print("\n" + "="*60)
    print(" Product Vision Board → Mermaid Diagram Generator")
    print("="*60 + "\n")

    # Print system information
    print_system_info()

    # Get configuration from environment
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    model_name = os.getenv("DEFAULT_MODEL")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    share = os.getenv("GRADIO_SHARE", "false").lower() == "true"

    # Validate HuggingFace token for transformers backend
    if sys.platform != "darwin" and not hf_token:
        print("\n⚠️  WARNING: HUGGINGFACE_TOKEN not found in environment!")
        print("For transformers backend, you need a HuggingFace token.")
        print("Get your token from: https://huggingface.co/settings/tokens")
        print("Then create a .env file with: HUGGINGFACE_TOKEN=hf_xxxxx\n")

        # Check if .env.template exists
        if os.path.exists(".env.template") and not os.path.exists(".env"):
            print("💡 Tip: Copy .env.template to .env and add your token\n")

    try:
        # Create analyzer
        print("🔧 Initializing model...")
        analyzer = create_analyzer(
            hf_token=hf_token,
            model_name=model_name,
            prefer_mlx=True  # Prefer MLX on macOS
        )
        print("✅ Model initialized successfully!\n")

        # Create and launch Gradio UI
        print("🚀 Launching Gradio interface...")
        demo = create_ui(analyzer)

        # Launch configuration
        launch_kwargs = {
            "server_port": server_port,
            "share": share,
            "show_error": True,
            "quiet": False
        }

        print(f"\n📍 Server will run on: http://localhost:{server_port}")
        if share:
            print("🌐 Public sharing enabled - a public URL will be generated")
        print("\n" + "="*60)
        print("🎉 Application ready! Open the URL above in your browser")
        print("="*60 + "\n")

        # Launch
        demo.launch(**launch_kwargs)

    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
