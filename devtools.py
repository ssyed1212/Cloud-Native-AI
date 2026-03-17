import os
import requests
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/devstral-2512:free"
def call_model(prompt: str):
response = requests.post(
"https://openrouter.ai/api/v1/chat/completions",
headers={
"Authorization": f"Bearer {API_KEY}",
"Content-Type": "application/json",
},
json={
"model": MODEL,
"messages": [
{"role": "user", "content": prompt}
],
},
)
return response.json()
if __name__ == "__main__":
result = call_model("Explain cloud-native systems in two sentences.")
print(result["choices"][0]["message"]["content"])