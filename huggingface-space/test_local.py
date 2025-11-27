#!/usr/bin/env python3
"""
Test script to run the Hugging Face Space version locally.
"""

import os
import sys

def check_environment():
    """Check if the environment is properly configured."""
    print("🔍 Checking environment...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]}")

    # Check for GPU (CUDA or MPS)
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA GPU available: {torch.cuda.get_device_name(0)}")
        elif torch.backends.mps.is_available():
            print("✅ Apple Silicon MPS available")
        else:
            print("⚠️ No GPU detected (CPU only)")
            print("   For better performance, use HF Spaces with ZeroGPU")
    except Exception as e:
        print(f"⚠️ Could not check GPU: {e}")

    print("\n💡 Note: ZeroGPU is only available on Hugging Face Spaces")
    print("   Local testing will use CPU/GPU if available")

    return True

def check_dependencies():
    """Check if required packages are installed."""
    print("\n🔍 Checking dependencies...")

    required_packages = [
        "gradio",
        "transformers",
        "torch",
        "spaces"
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            missing.append(package)

    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    return True

def main():
    """Run local tests."""
    print("📊 PVB Flow - Local Testing")
    print("=" * 60)

    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed")
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies check failed")
        sys.exit(1)

    print("\n✅ All checks passed!")
    print("\n🚀 Starting local server...")

    # Import and run the app
    try:
        from src.ui.spaces_interface import create_spaces_interface

        interface = create_spaces_interface()
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"\n❌ Failed to start app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
