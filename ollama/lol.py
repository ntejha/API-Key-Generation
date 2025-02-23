import ollama 

client = ollama.Client()

model = "mistral"
prompt = "What is Python ?"

response = client.generate(model=model, prompt=prompt)

print(response.response)