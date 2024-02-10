from config import TELEGRAM_TOKEN
from commands import commands
from questionnaire import ask_questionnaire_question, questionnaire_questions
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

def questionnaire_finished(update: Update, context: CallbackContext):
  update.message.reply_text("Спасибо за предоставленную информацию!")
  commands['menu'](update, context)

def handle_message(update: Update, context: CallbackContext):
  text = update.message.text
  print(text)
  user_data = context.user_data['data']
  is_answer = False
  for q in questionnaire_questions:
    if user_data[q['name']] == None:
      user_data[q['name']] = text
      is_answer = True
      if not ask_questionnaire_question(update, context):
        questionnaire_finished(update, context)
      break
  if not is_answer:
    update.message.reply_text("Шо?")

def handle_button(update: Update, context: CallbackContext):
  query = update.callback_query
  query.answer()
  data = query.data.split(':')
  print(data)
  if data[0] == "command":
    commands[data[1]](query, context)
    return

  user_data = context.user_data['data']
  user_data[data[0]] = data[1]
  if not ask_questionnaire_question(query, context):
    questionnaire_finished(query, context)

def main():
  updater = Updater(TELEGRAM_TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", commands['start']))
  dp.add_handler(CommandHandler("menu", commands['menu']))
  dp.add_handler(CommandHandler("assessment", commands['assessment']))
  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
  dp.add_handler(CallbackQueryHandler(handle_button))

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
