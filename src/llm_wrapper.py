import os
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class CPCoachLLM:
    """Wrapper for the Fine-tuned DeepSeek-Coder model using LangChain."""
    
    def __init__(self, model_path: str = "Qwen/Qwen2.5-Coder-7B-Instruct", adapter_path: str = "fine_tuning/cp-coach-finetuned", load_in_4bit: bool = True):
        self.model_path = model_path
        print(f"Loading LLM from {model_path}...")
        
        # Determine device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Load Model (with optional 4-bit quantization for lower VRAM usage)
        model_kwargs = {"device_map": "auto"}
        if load_in_4bit and device == "cuda":
            from transformers import BitsAndBytesConfig
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            model_kwargs["quantization_config"] = bnb_config

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            **model_kwargs
        )
        
        # Apply LoRA Adapter if it exists
        if adapter_path and os.path.exists(adapter_path):
            print(f"Applying LoRA adapter from {adapter_path}...")
            # from peft import PeftModel
            # self.model = PeftModel.from_pretrained(self.model, adapter_path) # تعطيل التدريب مؤقتاً
        
        # Create HuggingFace Pipeline
        self.hf_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=4096, # زيادة الـ tokens
            temperature=0.2, # Low temperature for more deterministic/logical outputs
            top_p=0.95,
            repetition_penalty=1.1,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Wrap in LangChain's HuggingFacePipeline
        self.llm = HuggingFacePipeline(pipeline=self.hf_pipeline)

    def get_llm(self):
        """Returns the LangChain LLM instance."""
        return self.llm
