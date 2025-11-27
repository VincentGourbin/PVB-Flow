"""
Transformers-based Mistral analyzer for cross-platform support.
Works on CPU, CUDA, and MPS (Apple Silicon).
"""
import gc
import torch
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM


class MistralTextAnalyzer:
    """
    Transformers-based Mistral model for diagram generation.
    Supports CUDA, MPS, and CPU backends.
    """

    def __init__(
        self,
        hf_token: str,
        model_name: str = "mistralai/Mistral-Small-Instruct-2409",
        load_in_8bit: bool = False
    ):
        """
        Initialize the Transformers Mistral analyzer.

        Args:
            hf_token: HuggingFace API token
            model_name: HuggingFace model ID
            load_in_8bit: Whether to load model in 8-bit mode (reduces memory)
        """
        self.model_name = model_name
        self.hf_token = hf_token
        self.load_in_8bit = load_in_8bit

        # Detect device and dtype
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.dtype = torch.float16
            print("✓ Using Apple Silicon (MPS) backend")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.dtype = torch.bfloat16
            print(f"✓ Using CUDA backend on {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device("cpu")
            self.dtype = torch.float32
            print("✓ Using CPU backend (slower)")

        # Load tokenizer and model
        self._load_model()

    def _load_model(self):
        """Load the model and tokenizer."""
        print(f"Loading model: {self.model_name}...")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=self.hf_token
        )

        # Load model
        if self.load_in_8bit and self.device.type != "cpu":
            # 8-bit quantization (requires bitsandbytes)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=self.hf_token,
                load_in_8bit=True,
                device_map="auto"
            )
        else:
            # Standard loading
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=self.hf_token,
                torch_dtype=self.dtype,
                device_map="auto" if self.device.type != "cpu" else None
            )
            if self.device.type == "cpu":
                self.model = self.model.to(self.device)

        print(f"✓ Model loaded on {self.device}")

    def generate_response(self, conversation: List[Dict[str, str]], max_tokens: int = 4000) -> str:
        """
        Generate response from conversation history.

        Args:
            conversation: List of conversation messages with 'role' and 'content'
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text
        """
        # Apply chat template
        prompt = self.tokenizer.apply_chat_template(
            conversation,
            tokenize=False,
            add_generation_prompt=True
        )

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.2,  # Low temperature for consistent diagrams
                do_sample=False,  # Greedy decoding for deterministic output
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response (skip input tokens)
        input_length = inputs["input_ids"].shape[1]
        response = self.tokenizer.decode(
            outputs[0][input_length:],
            skip_special_tokens=True
        )

        return response.strip()

    def cleanup_model(self):
        """Free model from memory."""
        if hasattr(self, 'model') and self.model is not None:
            self.model.to('cpu')
            del self.model
            self.model = None

        if hasattr(self, 'tokenizer') and self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        gc.collect()

        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        elif torch.cuda.is_available():
            torch.cuda.empty_cache()

        print("✓ Transformers model cleaned up")
