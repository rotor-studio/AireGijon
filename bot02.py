import os
import telebot
import requests
import json

#API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API)

sensores = [72384,64120,72289,73510,73768,69414,72437,60233,73213,73219,70332,73138,71637,71191,69703,72424]

#Para leer lo que te envía un sensor
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj,sort_keys=True, indent=4)
    print(text)

@bot.message_handler(commands=['test'])
def hola(message):
    response = requests.get("https://data.sensor.community/airrohr/v1/sensor/72384/")
    pilla = response.json()
    jprint(pilla)
    bot.reply_to(message, "list")

@bot.message_handler(commands=['sensores'])
def sen(message):
    for d in sensores:
     bot.send_message(message.chat.id,d)


@bot.message_handler(commands=['este'])
def yeah(message):
    response = requests.get("https://data.sensor.community/airrohr/v1/sensor/73768/")

    print(response.json()[0]["location"]["latitude"])

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    pilla = []

    for d in sensores:
        if message.text in str(d):
            try:
             sens = "https://data.sensor.community/airrohr/v1/sensor/"
             slash = "/"
             f = sens+str(d)+slash
             response = requests.get(f)
             pilla.append(response.json()[0]["sensordatavalues"][0]["value"])
             pilla.append(response.json()[0]["sensordatavalues"][1]["value"])
             pilla.append(response.json()[0]["location"]["latitude"])
             pilla.append(response.json()[0]["location"]["longitude"])
             bot.send_location(message.chat.id, latitude=pilla[2], longitude=pilla[3])

             print("Ahora mismo el valor de PM10 es: "+pilla[0]+"| el de PM2.5 es: "+pilla[1])
             v = "Ahora mismo el valor de PM10 es: "
             v2 = " | El de PM2.5 es: "
             v3 = v + pilla[0] + v2 + pilla[1]
             bot.send_message(message.chat.id, v3)

            except:
             print("No encontré nada!")
             v3 = "No encontré nada!"
             bot.send_message(message.chat.id, v3)



bot.polling()
