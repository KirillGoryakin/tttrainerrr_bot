from telegram import Update
from telegram.ext import CallbackContext
from utils import ask_yandex_gpt, ask_gpt_vision, questionnaire_to_string

def food_assessment_handler(update: Update, context: CallbackContext):
  photo_file = update.message.photo[-1].get_file()
  photo_file_path = f'./db/img/{photo_file.file_id}.jpg'
  photo_file.download(photo_file_path)
  food_list = ask_gpt_vision(
    "User sends you a picture of their food. You need to list every food you can see on the picture. Do not mention any counties, it's history or anything not related to the food itself. If you cannot see any food on the picture just say \"I can't see any food on the picture.\"",
    photo_file_path,
  )
  print(food_list)
  result = ask_yandex_gpt(
    "Тебе дано текстовое описание фотографии с едой на английском языке, а так же анкета пользователя о его состоянии и питании. Переведи описание еды на русский язык. Если в описании написано, что на фото не видно еды, то переведи это сообщение и заканчивай. Если это описание еды, то в первом абзаце напиши перевод этого описания на русский язык, а во втором абзаце оцени, как такое питание повлияет на пользователя с учётом его ответов в анкете, и что ему может быть следует поменять в своём питании. Не нужно описавать или повторять всю анкету, но на неё нужно ссылаться для обоснавания своего совета. Не более 3-4 предложений. В своём ответе обращайся к пользователю на Ты, в неформальном стиле.",
f"""{food_list}
{questionnaire_to_string(context.user_data['data'])}
"""
  )
  print(result)
  update.message.reply_text(result)

handlers = {
  "food_assessment": food_assessment_handler
}