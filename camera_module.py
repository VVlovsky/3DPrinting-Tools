import cv2
import telebot
import os
import numpy as np
from time import sleep

with open("config.json", "rb") as read_file:
    TOKEN = json.load(read_file)['TOKEN']
    white_list = json.load(read_file)['white_list']


bot = telebot.TeleBot(TOKEN, threaded=False)

def cap_video(duration: int):
    cap = cv2.VideoCapture(2)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('buffer.mp4',fourcc, 10.0, (640,480))

    frames_total = 10 * duration
    for _ in range(frames_total):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        else:
            break
    cap.release()
    out.release()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "hey debug")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'инфо':
        name = 'buffer'
        camera = cv2.VideoCapture(2)

        sleep(3)

        return_value, image = camera.read()
        cv2.imwrite(f'./{name}.png', image)
        bot.send_photo(message.chat.id, photo=open(f'./{name}.png', 'rb'))

        camera.release()
        os.remove(f'./{name}.png')

    elif 'инфострим' in message.text.lower():
        if message.from_user.username not in white_list:
            bot.send_message(message.chat.id, 'ты кто такой? я тебя не знаю')
        else:
            duration = int(message.text.split(' ')[-1])
            cap_video(duration)
            bot.send_video_note(message.chat.id, open(f'./buffer.mp4', 'rb'))
            os.remove(f'./buffer.mp4')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
cv2.destroyAllWindows()

