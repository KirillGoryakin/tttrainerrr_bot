from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import CallbackContext

questionnaire_questions = [
  { "name": "sex", "text": "Ваш пол", "options": ["Мужской", "Женский"] },
  { "name": "age", "text": "Сколько вам полных лет?\n_В ответе напишите только число_", "options": [] },
  { "name": "weight", "text": "Какой ваш вес в килограммах?\n_В ответе напишите только число_", "options": [] },
  { "name": "height", "text": "Какой ваш рост в сантиметрах?\n_В ответе напишите только число_", "options": [] },
  { "name": "meal_frequency", "text": "Сколько раз в день вы обычно питаетесь?", "options": [] },
  { "name": "meal_description", "text": "Кратко опишите, что вы обычно едите во время каждого приёма пищи.", "options": [] },
  { "name": "physical_activity", "text": "Вы занимаетесь физической активностью? Если да, то как часто и что вы обычно делаете?", "options": [] },
]

# returns True = has more questions; False = no more questions
def ask_questionnaire_question(update: Update, context: CallbackContext):
  user_data = context.user_data['data']
  # Ask one question that was not answere before
  for i in range(len(questionnaire_questions)):
    question = questionnaire_questions[i]
    if user_data[question['name']] == None:
      reply_markup = None
      if len(question['options']) > 0:
        reply_markup = InlineKeyboardMarkup(
          list(map(lambda o: [
            InlineKeyboardButton(o, callback_data=f"{question['name']}:{o}")
          ], question['options']))
        )

      reply = f"*{i+1}.* {question['text']}"
      print(reply)
      update.message.reply_text(reply, reply_markup=reply_markup, parse_mode=PARSEMODE_MARKDOWN)
      return i + 1 <= len(questionnaire_questions)
  
  return False