from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
from auto_gptq import AutoGPTQForCausalLM
model = AutoGPTQForCausalLM.from_quantized("textminr/llama-2-7b-chat-4bit-gptq")

# model = "textminr/llama-2-7b-4bit-gptq"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat32,
    trust_remote_code=True,
    device_map="auto",
)
sequences = pipeline(
   "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
