import telebot
import os
from dotenv import load_dotenv


load_dotenv()

# You need to change API TOKEN to your token
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Hi there, I am Auto Link Adder created by Farkhod. I am here to add a link to your post automatically!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    link = 'https://t.me/IT_Memes_Programmers'
    text = '👉 IT-MEMES'
    new_message = "For using just send the picture and write whatever description " + "\n\n" + 'Join <a href="' + link + '">' + text + '</a>'
    bot.send_message(chat_id=message.chat.id, text=new_message, parse_mode="HTML")


# handle all photos
@bot.message_handler(func=lambda message: True, content_types=['photo'])
def handle_photo(message):

    # Get the photo with ID
    photo_id = bot.get_file(message.photo[-1].file_id)

    # Download the photo
    photo_file = bot.download_file(photo_id.file_path)

    # Save the photo to disk
    with open('img/photo.jpg', 'wb') as f:
        f.write(photo_file)

    # Texts that should be added
    link = 'https://t.me/IT_Memes_Programmers'
    text = '👉 IT-MEMES'

    # Edit the message caption
    new_caption = message.caption + "\n\n" + '<a href="' + link + '">' + text + '</a>'

    # Send the photo again with the new caption
    f = open('img/photo.jpg', 'rb')
    channel_id = os.getenv("channel_id")
    bot.send_photo(chat_id=channel_id, photo=f, caption=new_caption, parse_mode="HTML")


bot.infinity_polling()