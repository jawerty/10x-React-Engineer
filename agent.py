from transformers import AutoTokenizer
import transformers
import torch

class Agent:
  def __init__(self):
    model = "meta-llama/Llama-2-13b-chat-hf"
    self.tokenizer = AutoTokenizer.from_pretrained(model)
    self.pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
  def generate(self, prompt):
    sequences = self.pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=self.tokenizer.eos_token_id,
        max_length=10000,
    )
    return sequences[0]['generated_text']