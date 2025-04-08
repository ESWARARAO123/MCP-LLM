from transformers import pipeline

# Load a pre-trained language model
llm = pipeline("text-generation", model="distilgpt2")

def generate_response(prompt):
    response = llm(prompt, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']