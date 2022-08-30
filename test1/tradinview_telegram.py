import requests

def telegram_send_text(bot_message,id):
    bot_token = "yourbotid"
    bot_chatID = id
    send_text = "https://api.telegram.org/bot" + bot_token + "/sendmessage?chat_id=" + bot_chatID + "&parse_mode" + "=Markdown&text=" + bot_message

    response = requests.get(send_text)
    return response.json()
    
telegram_send_text("test text","yourchatid")