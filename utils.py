from config import YANDEX_TOKEN, FOLDER_ID, OPENAI_API_KEY
import requests
import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

yandex_headers = {
  "Content-Type": "application/json",
  "Authorization": f"Api-Key {YANDEX_TOKEN}"
}

def ask_yandex_gpt(system: str, text: str):
  response = requests.post(
    "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    headers=yandex_headers,
    json={
      "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
      "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "700"
      },
      "messages": [
        { "role": "system", "text": system },
        { "role": "user", "text": text },
      ]
    }
  ).json()
  return (
    response
      .get('result', {})
      .get('alternatives', [{}])[0]
      .get('message', {})
      .get('text', 'YandexGPT не захотел отвечать :(\nПопробуйте позже')
  )

openai_headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPENAI_API_KEY}"
}

def ask_gpt_vision(system: str, image_path: str):
  base64_image = encode_image(image_path)
  response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=openai_headers,
    json={
      "model": "gpt-4-vision-preview",
      "messages": [
        { "role": "system", "content": system },
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low",
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }
  ).json()
  return (
    response
      .get('choices', [])[0]
      .get('message', {})
      .get('content', 'Something went wrong wiht ChatGPT vision...\nPlease try again')
  )

def questionnaire_to_string(user_data: dict):
  return f"""
Анкета.
Пол: "{user_data['sex']}"
Возраст: "{user_data['age']}"
Вес в килограммах: "{user_data['weight']}"
Рост в сантиметрах: "{user_data['height']}"
Сколько раз в день вы обычно питаетесь: "{user_data['meal_frequency']}"
Кратко опишите, что вы обычно едите во время каждого приёма пищи: "{user_data['meal_description']}"
Вы занимаетесь физической активностью? Если да, то как часто и что вы обычно делаете: "{user_data['physical_activity']}"
"""