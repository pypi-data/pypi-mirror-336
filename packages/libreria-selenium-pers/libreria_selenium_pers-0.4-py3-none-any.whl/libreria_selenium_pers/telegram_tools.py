import requests
import os

API_KEY = os.getenv('TELEGRAM_BOT_TOKEN')
MESSAGE_ID = os.getenv('TELEGRAM_CHAT_ID')

#This function receives a message and send it by Telegram with the given variables.
#Param: message, the message that is going to be send.
def sendMessage(message):
    send_text = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + MESSAGE_ID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response