import requests

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "AIzaSyD96p0ZoA6LOvmlH75xRAzYLiECcGew5_0"

def get_gemini_response(face_emotion, text_emotion, spoken_text):
    prompt = (
        f"The user's facial emotion is '{face_emotion}', "
        f"their spoken text emotion is '{text_emotion}', "
        f"and the spoken text is: \"{spoken_text}\".\n"
        "Respond empathetically as a therapy assistant to this user."
    )

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-2.5-flash",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get("choices", [{}])[0].get("text", "Sorry, no response.")
    else:
        print(f"Gemini API Error: {response.status_code} {response.text}")
        return "Sorry, I am unable to respond right now."
