"""
Factory for creating the best available analyzer based on platform and available libraries.
"""
import sys
import platform


def create_analyzer(
    hf_token: str = None,
    model_name: str = None,
    prefer_mlx: bool = True
):
    """
    Auto-detect best backend and create appropriate analyzer.

    Strategy:
    1. On macOS: Try MLX first (fastest, lowest memory), fallback to transformers
    2. On Linux/Windows: Use transformers with CUDA/CPU

    Args:
        hf_token: HuggingFace API token (required for transformers backend)
        model_name: Override default model name
        prefer_mlx: If True and on macOS, try MLX first

    Returns:
        Analyzer instance (MistralMLXAnalyzer or MistralTextAnalyzer)
    """
    # Determine default model name
    if model_name is None:
        if sys.platform == "darwin" and prefer_mlx:
            model_name = "mlx-community/Mistral-Small-3.1-24B-Instruct-2503-8bit"
        else:
            model_name = "mistralai/Mistral-Small-Instruct-2409"

    # On macOS, try MLX first
    if sys.platform == "darwin" and prefer_mlx:
        try:
            from .mistral_mlx_analyzer import MistralMLXAnalyzer
            print("🚀 Using MLX backend (optimized for Apple Silicon)")
            return MistralMLXAnalyzer(model_name=model_name)
        except ImportError as e:
            print(f"⚠️  MLX not available: {e}")
            print("📦 Falling back to transformers backend...")
        except Exception as e:
            print(f"⚠️  MLX initialization failed: {e}")
            print("📦 Falling back to transformers backend...")

    # Fallback to transformers (cross-platform)
    from .mistral_text_analyzer import MistralTextAnalyzer

    if hf_token is None:
        raise ValueError(
            "HuggingFace token required for transformers backend. "
            "Get your token from https://huggingface.co/settings/tokens "
            "and set it in the HUGGINGFACE_TOKEN environment variable."
        )

    print("🚀 Using Transformers backend (cross-platform)")
    return MistralTextAnalyzer(
        hf_token=hf_token,
        model_name=model_name,
        load_in_8bit=True  # Use 8-bit to reduce memory
    )


def get_system_info() -> dict:
    """
    Get system information for debugging.

    Returns:
        Dictionary with system details
    """
    info = {
        "platform": sys.platform,
        "python_version": platform.python_version(),
        "machine": platform.machine(),
    }

    # Check for GPU availability
    try:
        import torch
        info["torch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        info["mps_available"] = torch.backends.mps.is_available()
        if torch.cuda.is_available():
            info["cuda_device"] = torch.cuda.get_device_name(0)
    except ImportError:
        info["torch_available"] = False

    # Check for MLX availability
    try:
        import mlx
        info["mlx_available"] = True
        try:
            info["mlx_version"] = mlx.__version__
        except AttributeError:
            info["mlx_version"] = "installed (version unknown)"
    except ImportError:
        info["mlx_available"] = False

    return info


def print_system_info():
    """Print system information for debugging."""
    info = get_system_info()

    print("\n" + "=" * 50)
    print("SYSTEM INFORMATION")
    print("=" * 50)

    for key, value in info.items():
        print(f"{key:20s}: {value}")

    print("=" * 50 + "\n")
