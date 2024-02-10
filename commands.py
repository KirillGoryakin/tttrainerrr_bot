from questionnaire import ask_questionnaire_question
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import CallbackContext
from utils import ask_yandex_gpt

initial_user_data = {
  "sex": None,
  "age": None,
  "weight": None,
  "height": None,
  "meal_frequency": None,
  "meal_description": None,
  "physical_activity": None,
}

def start(update: Update, context: CallbackContext):
  print("/start")
  chat = update.message.chat
  context.user_data.clear()
  context.user_data['data'] = initial_user_data.copy()
  update.message.reply_text(f"Привет, *{chat.first_name}*! Я бот, который использует YandexGPT для ответов на ваши вопросы. Для начала заполните анкету.", parse_mode=PARSEMODE_MARKDOWN)
  ask_questionnaire_question(update, context)

def menu(update: Update, context: CallbackContext):
  print("/menu")
  update.message.reply_text(
    "*Меню*",
    parse_mode=PARSEMODE_MARKDOWN,
    reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("Пройти анкету заново", callback_data="command:start")],
      [InlineKeyboardButton("✨ Оценить своё состояние", callback_data="command:assessment")],
    ]),
  )

def assessment(update: Update, context: CallbackContext):
  print("/assessment")
  user_data = context.user_data['data']
  result: str = ask_yandex_gpt(
    "Ты играешь роль тренера и диетолога. Пользователь заполнил анкету о своём состоянии. На основе его ответов ты должен дать оценку его состоянию здоровья и образу жизни и дать пару советов. Твой ответ должнен состоять из 1-2 предложений с твоей оценкой. Далее идут твои советы, но не слишком много, не более 4 предложений. В своём ответе обращайся к пользователю на Ты, в неформальном стиле.",
f"""
Анкета.
Пол: "{user_data['sex']}"
Возраст: "{user_data['age']}"
Вес в килограммах: "{user_data['weight']}"
Рост в сантиметрах: "{user_data['height']}"
Сколько раз в день вы обычно питаетесь: "{user_data['meal_frequency']}"
Кратко опишите, что вы обычно едите во время каждого приёма пищи: "{user_data['meal_description']}"
Вы занимаетесь физической активностью? Если да, то как часто и что вы обычно делаете: "{user_data['physical_activity']}"
""",
  )
  print(result)
  update.message.reply_text(result.replace("**", "*"), parse_mode=PARSEMODE_MARKDOWN)
  

commands = {
  "start": start,
  "menu": menu,
  "assessment": assessment,
}