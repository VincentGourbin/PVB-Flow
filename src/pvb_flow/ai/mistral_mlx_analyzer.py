"""
MLX-based Mistral analyzer for Apple Silicon (M1/M2/M3).
Optimized for fast inference with lower memory usage.
"""
import gc
from typing import List, Dict


class MistralMLXAnalyzer:
    """
    MLX-optimized Mistral model for diagram generation.
    Uses mlx-lm library for efficient inference on Apple Silicon.
    """

    def __init__(self, model_name: str = "mlx-community/Mistral-Small-3.1-24B-Instruct-2503-8bit"):
        """
        Initialize the MLX Mistral analyzer.

        Args:
            model_name: HuggingFace model ID (default: Mistral-Small-3.1-24B-Instruct-2503-8bit)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def _load_model(self):
        """Lazy load the model and tokenizer."""
        if self.model is None or self.tokenizer is None:
            try:
                from mlx_lm import load
                # Load model with tokenizer config
                self.model, self.tokenizer = load(
                    self.model_name,
                    tokenizer_config={"fix_mistral_regex": True}
                )
                print(f"✓ MLX model loaded: {self.model_name}")
            except ImportError as e:
                raise ImportError(
                    "mlx-lm not installed. Install with: pip install mlx-lm\n"
                    "Note: MLX only works on Apple Silicon (M1/M2/M3)"
                ) from e

    def generate_response(self, conversation: List[Dict[str, str]], max_tokens: int = 4000) -> str:
        """
        Generate response from conversation history.

        Args:
            conversation: List of conversation messages with 'role' and 'content'
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text
        """
        self._load_model()

        from mlx_lm import generate
        from mlx_lm.sample_utils import make_sampler

        # Try to use apply_chat_template if available
        try:
            prompt = self.tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
        except (AttributeError, ValueError):
            # Fallback: manual Mistral Instruct format
            prompt = self._format_mistral_chat(conversation)

        # Create sampler with low temperature for consistent diagram generation
        sampler = make_sampler(temp=0.2)

        # Generate response
        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            sampler=sampler,
            verbose=False
        )

        return response.strip()

    def _format_mistral_chat(self, conversation: List[Dict[str, str]]) -> str:
        """
        Manually format conversation for Mistral Instruct models.

        Mistral Instruct format:
        <s>[INST] user message [/INST] assistant response</s>[INST] user message [/INST]

        Args:
            conversation: List of messages with 'role' and 'content'

        Returns:
            Formatted prompt string
        """
        prompt_parts = []

        for i, msg in enumerate(conversation):
            if msg["role"] == "user":
                prompt_parts.append(f"[INST] {msg['content']} [/INST]")
            elif msg["role"] == "assistant":
                prompt_parts.append(msg['content'])

        # Build final prompt
        if len(prompt_parts) > 0:
            result = "<s>"
            for i, part in enumerate(prompt_parts):
                if i > 0 and "[INST]" in part:
                    result += "</s>"
                result += part
                if i < len(prompt_parts) - 1 and "[INST]" not in prompt_parts[i + 1]:
                    result += " "
            return result

        return ""

    def cleanup_model(self):
        """Free model from memory."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        gc.collect()
        print("✓ MLX model cleaned up")
