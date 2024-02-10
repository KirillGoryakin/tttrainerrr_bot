from config import YANDEX_TOKEN, FOLDER_ID
import requests

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Api-Key {YANDEX_TOKEN}"
}
completionOptions = {
  "stream": False,
  "temperature": 0.6,
  "maxTokens": "700"
}

def ask_yandex_gpt(system: str, text: str):
  response = requests.post(
    "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    headers=headers,
    json={
      "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
      "completionOptions": completionOptions,
      "messages": [
        {
          "role": "system",
          "text": system
        },
        {
          "role": "user",
          "text": text
        }
      ]
    }
  ).json()
  return response.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', 'Упс... Что-то пошло не так :(')