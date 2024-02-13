from questionnaire import ask_questionnaire_question
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import CallbackContext
from utils import ask_yandex_gpt, questionnaire_to_string

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
  context.user_data['state'] = "questionnaire"
  update.message.reply_text(f"Привет, *{chat.first_name}*! Я бот, который использует YandexGPT для ответов на твои вопросы. Для начала заполни анкету.", parse_mode=PARSEMODE_MARKDOWN)
  ask_questionnaire_question(update, context)

def menu(update: Update, context: CallbackContext):
  print("/menu")
  update.message.reply_text(
    "*Меню*",
    parse_mode=PARSEMODE_MARKDOWN,
    reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("Пройти анкету заново", callback_data="command:start")],
      [InlineKeyboardButton("✨ Оценить своё состояние", callback_data="command:assessment")],
      [InlineKeyboardButton("✨ Оценить свою еду по фото", callback_data="command:food_assessment")],
    ]),
  )

def assessment(update: Update, context: CallbackContext):
  print("/assessment")
  user_data = context.user_data['data']
  result: str = ask_yandex_gpt(
    "Ты играешь роль тренера и диетолога. Пользователь заполнил анкету о своём состоянии. На основе его ответов ты должен дать оценку его состоянию здоровья и образу жизни и дать пару советов. Твой ответ должнен состоять из 1-2 предложений с твоей оценкой. Далее идут твои советы, но не слишком много, не более 4 предложений. В своём ответе обращайся к пользователю на Ты, в неформальном стиле.",
    questionnaire_to_string(user_data),
  )
  print(result)
  update.message.reply_text(result.replace("**", "*"), parse_mode=PARSEMODE_MARKDOWN)
  
def food_assessment(update: Update, context: CallbackContext):
  context.user_data['state'] = "food_assessment"
  update.message.reply_text("Давай я оценю твою хавку. Кидай фотку 📷")

commands = {
  "start": start,
  "menu": menu,
  "assessment": assessment,
  # "food_assessment": food_assessment,
}