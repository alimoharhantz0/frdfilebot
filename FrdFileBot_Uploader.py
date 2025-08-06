
import requests
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '8057986115:AAEyj4IMZveQmABmQl_3XtaE2pNb4wQhQHU'

def upload_to_gofile(file_path):
    server_resp = requests.get('https://api.gofile.io/getServer').json()
    server = server_resp['data']['server']

    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f'https://{server}.gofile.io/uploadFile', files=files)
    return response.json()['data']['downloadPage']

def handle_file(update, context):
    file = update.message.document.get_file()
    file_path = file.download()

    try:
        link = upload_to_gofile(file_path)
        update.message.reply_text('✅ فایل آپلود شد:\n' + link)
    except Exception as e:
        update.message.reply_text('❌ خطا در آپلود: ' + str(e))

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.document, handle_file))
updater.start_polling()
updater.idle()
