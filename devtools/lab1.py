import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")
# MODEL = "mistralai/devstral-2512:free"
MODEL = "mistralai/devstral-2512"

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
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY is not set in your environment.")
        exit(1)
    result = call_model("Explain cloud-native systems in two sentences.")
    if "error" in result:
        print("API error:", result["error"].get("message", result["error"]))
    elif "choices" in result and result["choices"]:
        print(result["choices"][0]["message"]["content"])
    else:
        print("Unexpected response:", result)
