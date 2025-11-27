#!/usr/bin/env python3
"""
HuggingFace Spaces Deployment Script for PVB Flow
Deploys the PVB Flow app to HuggingFace Spaces with Mistral API support
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import getpass

# Configuration
SPACE_NAME = "VincentGOURBIN/PVB-Flow-Mermaid-Generator"
SPACE_TITLE = "📊 PVB Flow - Product Vision Board to Mermaid"
SPACE_DESCRIPTION = "Transform Product Vision Boards into professional Mermaid diagrams with Qwen3-4B & ZeroGPU"

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")

    # Check git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install git first.")
        sys.exit(1)

    # Check huggingface_hub
    try:
        import huggingface_hub
        print("✅ HuggingFace Hub is available")
    except ImportError:
        print("❌ HuggingFace Hub not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], check=True)
        print("✅ HuggingFace Hub installed")

def get_hf_token():
    """Get HuggingFace token from environment or user input"""
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")

    if not token:
        print("\n🔑 HuggingFace token required for deployment")
        print("You can get your token from: https://huggingface.co/settings/tokens")
        print("Make sure your token has 'write' permissions")
        token = getpass.getpass("Enter your HuggingFace token: ").strip()

    if not token:
        print("❌ No token provided. Deployment cancelled.")
        sys.exit(1)

    return token

def create_space_config():
    """Create the Space configuration files"""
    print("📝 Creating Space configuration...")

    # README.md already exists, just verify
    if not os.path.exists("README.md"):
        print("❌ README.md not found. Please ensure README.md exists.")
        sys.exit(1)

    print("✅ Space configuration validated")

def validate_files():
    """Validate that all required files exist"""
    print("🔍 Validating files...")

    required_files = [
        "app.py",
        "requirements.txt",
        "README.md"
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        sys.exit(1)

    print("✅ All required files present")

def validate_source_structure():
    """Validate the source code structure"""
    print("🔍 Validating source structure...")

    required_dirs = [
        "src/"
    ]

    required_source_files = [
        "src/ui/spaces_interface.py",
        "src/ai/qwen_zerogpu_analyzer.py"
    ]

    missing_items = []

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_items.append(dir_path)

    for file_path in required_source_files:
        if not os.path.exists(file_path):
            missing_items.append(file_path)

    if missing_items:
        print(f"❌ Missing required source items: {', '.join(missing_items)}")
        print("\n💡 Make sure you're running this script from the huggingface-space directory")
        print("   and that all source files have been copied to src/")
        sys.exit(1)

    print("✅ Source structure validated")

def create_space(token):
    """Create or update the HuggingFace Space"""
    print(f"🚀 Creating/updating Space: {SPACE_NAME}")

    from huggingface_hub import HfApi, login

    # Login to HuggingFace
    login(token=token, add_to_git_credential=True)

    api = HfApi()

    try:
        # Try to get space info (check if it exists)
        space_info = api.space_info(repo_id=SPACE_NAME)
        print(f"✅ Space {SPACE_NAME} already exists, updating...")
        update_mode = True
    except Exception:
        print(f"📦 Creating new Space: {SPACE_NAME}")
        update_mode = False

        # Create the space
        try:
            api.create_repo(
                repo_id=SPACE_NAME,
                repo_type="space",
                space_sdk="gradio",
                private=False
            )
            print("✅ Space created successfully")
        except Exception as e:
            print(f"❌ Failed to create space: {e}")
            sys.exit(1)

    return update_mode

def deploy_files(token):
    """Deploy files to the Space"""
    print("📤 Uploading files to Space...")

    from huggingface_hub import HfApi

    api = HfApi()

    # Files to upload
    files_to_upload = [
        "app.py",
        "requirements.txt",
        "README.md"
    ]

    # Directories to upload recursively
    dirs_to_upload = [
        "src/"
    ]

    try:
        # Upload individual files
        for file in files_to_upload:
            if os.path.exists(file):
                print(f"  📄 Uploading {file}...")
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=SPACE_NAME,
                    repo_type="space",
                    token=token
                )
            else:
                print(f"  ⚠️ Skipping missing file: {file}")

        # Upload directories
        for dir_path in dirs_to_upload:
            if os.path.exists(dir_path):
                print(f"  📁 Uploading directory {dir_path}...")
                api.upload_folder(
                    folder_path=dir_path,
                    path_in_repo=dir_path,
                    repo_id=SPACE_NAME,
                    repo_type="space",
                    token=token,
                    ignore_patterns=["__pycache__", "*.pyc", ".DS_Store", "*.md"]
                )
            else:
                print(f"  ⚠️ Skipping missing directory: {dir_path}")

        print("✅ All files uploaded successfully")

    except Exception as e:
        print(f"❌ Failed to upload files: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def set_space_secrets(token):
    """Set required secrets for the Space"""
    print("\n🔐 Space secrets configuration...")
    print("✅ No secrets required - using ZeroGPU with Qwen model")
    print("   The model will be loaded automatically from Hugging Face Hub")

def wait_for_space_build():
    """Wait for the space to build"""
    print("\n⏳ Space is building... This may take a few minutes.")
    print(f"🌐 You can monitor the build at: https://huggingface.co/spaces/{SPACE_NAME}")
    print("📱 The space will be available once the build completes.")

def main():
    """Main deployment function"""
    print("📊 PVB Flow - HuggingFace Spaces Deployment")
    print("=" * 60)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Check dependencies
    check_dependencies()

    # Get HuggingFace token
    token = get_hf_token()

    # Validate source structure
    validate_source_structure()

    # Create space configuration
    create_space_config()

    # Validate files
    validate_files()

    # Create or update space
    update_mode = create_space(token)

    # Deploy files
    deploy_files(token)

    # Set secrets
    set_space_secrets(token)

    # Success message
    print("\n🎉 Deployment completed successfully!")
    print(f"🌐 Space URL: https://huggingface.co/spaces/{SPACE_NAME}")

    if not update_mode:
        wait_for_space_build()

    print(f"\n📱 Your PVB Flow app is now live at:")
    print(f"   https://huggingface.co/spaces/{SPACE_NAME}")
    print(f"\n🚀 Transform Product Vision Boards into Mermaid diagrams!")
    print("\n📊 Happy diagram generating! ✨")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
