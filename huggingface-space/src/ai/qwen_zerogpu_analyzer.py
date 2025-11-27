"""
Qwen3-VL model with ZeroGPU support for Hugging Face Spaces.
Uses transformers with @spaces.GPU decorator.
"""
import torch
from typing import List, Dict
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
import spaces


class QwenZeroGPUAnalyzer:
    """
    Qwen3 model analyzer with ZeroGPU support.
    Uses Qwen3-VL-4B-Instruct for diagram generation.
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-VL-4B-Instruct"
    ):
        """
        Initialize the Qwen ZeroGPU analyzer.

        Args:
            model_name: HuggingFace model ID
        """
        self.model_name = model_name
        self.model = None
        self.processor = None

        print(f"✓ Qwen ZeroGPU analyzer initialized (model will load on first inference)")
        print(f"  Model: {self.model_name}")

    def _load_model(self):
        """Load model and processor (called on first inference)."""
        if self.model is not None:
            return

        print(f"Loading model: {self.model_name}...")

        # Load processor (for Qwen3-VL)
        self.processor = AutoProcessor.from_pretrained(
            self.model_name
        )

        # Load model (Qwen3-VL model)
        self.model = Qwen3VLForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype="auto",  # Use auto dtype like in official example
            device_map="auto"
        )

        print(f"✓ Model loaded: {self.model_name}")

    @spaces.GPU(duration=60)  # ZeroGPU decorator - max 60 seconds
    def generate_response(self, conversation: List[Dict[str, str]], max_tokens: int = 4000) -> str:
        """
        Generate response from conversation history using ZeroGPU.

        Args:
            conversation: List of conversation messages with 'role' and 'content'
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text
        """
        # Load model on first call
        if self.model is None:
            self._load_model()

        # Format conversation for Qwen3-VL (text-only usage)
        # Build prompt from conversation history
        messages = []
        for msg in conversation:
            role = msg["role"]
            content = msg["content"]

            # Qwen3-VL expects specific format
            messages.append({
                "role": role,
                "content": [{"type": "text", "text": content}]
            })

        # Apply chat template (following official example)
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )
        inputs = inputs.to(self.model.device)

        # Generate with ZeroGPU (following official example)
        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens
        )

        # Trim generated ids (remove input tokens)
        generated_ids_trimmed = [
            out_ids[len(in_ids):]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        # Decode response
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        return output_text[0].strip()

    def cleanup_model(self):
        """Cleanup (managed by ZeroGPU)."""
        # ZeroGPU handles cleanup automatically
        pass
