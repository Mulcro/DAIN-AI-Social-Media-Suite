import os
from transformers import (AutoModelForCausalLM, AutoTokenizer)
import torch

print('buidling model...')
model = 'facebook/bart-large-cnn'
llm = AutoModelForCausalLM.from_pretrained(model)
tokenizer = AutoTokenizer.from_pretrained(model)
tokenizer.pad_token = tokenizer.eos_token

transcript_path = os.path.join("components", "transcript.txt")
transcript_open = open(transcript_path, "r")
transcript = transcript_open.read()
# prompt = 'Pick out 3 highlight worthy moments that would perform well on social media for short form content from the following video transcript: ' + transcript
prompt = "Give 3 facts about California:"
prompt_input_ids = tokenizer.encode(prompt, return_tensors='pt')
prompt_am = torch.ones(prompt_input_ids.shape, dtype=torch.long)  # Create attention mask

llm_output = llm.generate(
    prompt_input_ids,
    max_length=500,
    num_return_sequences=1,
    do_sample=True,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
    attention_mask=prompt_am,
    repetition_penalty=1.2)

decoded_response = tokenizer.decode(llm_output[0], skip_special_tokens=True)
print(decoded_response)