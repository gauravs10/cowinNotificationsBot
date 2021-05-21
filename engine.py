import time

import keys, database, utils, flask, telegram, schedule, datetime
from flask import Flask
primitiveInput = keys.main()
primitiveInput.flaskApp = Flask(__name__)

def dbCheck():
    if isinstance(primitiveInput.formattedResult ,list):
        for statement in primitiveInput.formattedResult:
            database.selectDbCommand(primitiveInput, statement)
            if len(primitiveInput.postGresDB.fetchall()) != 1:
                primitiveInput.telegramBot.sendMessage(chat_id = primitiveInput.telegramChatID, text = statement)
                database.insertDbCommand(primitiveInput, statement)
                database.commitDBConn(primitiveInput)
            else:
                pass
        database.dbClose(primitiveInput)
    else:
        pass

@primitiveInput.flaskApp.route(f'/{primitiveInput.telegramToken}', methods = ['POST'])
def engine():
    primitiveInput.telegramMsg = telegram.Update.de_json(flask.request.get_json(force = True), primitiveInput.telegramBot)
    primitiveInput.telegramChatID = primitiveInput.telegramMsg.message.chat_id
    primitiveInput.telegramMsgID = primitiveInput.telegramMsg.message.message_id

    telegramText = primitiveInput.telegramMsg.message.text.encode('utf-8').decode()
    if telegramText == '/start':
        bot_welcome = """   Welcome to Cowin Notifications Bot. This bot can be used enable notifications for vaccine slots on https://www.cowin.gov.in/home for pre-set filters or custom filters. Please enter /scanner1 to start notifications for South East Delhi for 18 + age group """
        primitiveInput.telegramBot.sendMessage(chat_id = primitiveInput.telegramChatID, text = bot_welcome, reply_to_message_id = primitiveInput.telegramMsgID)

    elif telegramText == '/scanner1':
        utils.setAttributes(primitiveInput, '9', '144', '18', datetime.datetime.today().strftime('%d-%m-%y'))
        primitiveInput.districts = utils.fetchAllDistricts(primitiveInput)
        utils.get_availability_by_district(primitiveInput)
        primitiveInput.Flag = True
        schedule.every().seconds.do(dbCheck)
        while primitiveInput.Flag:
            schedule.run_pending()
            time.sleep(30)
            print(primitiveInput.formattedResult)
            print(primitiveInput.filteredOutputByAge)
            abc = telegram.Update.de_json(flask.request.get_json(force=True), primitiveInput.telegramBot)
            print(abc.message.text.encode('utf-8').decode())
            #
            # if isinstance(primitiveInput.formattedResult, dict):
            #     if len(primitiveInput.formattedResult) > 0:
            #         primitiveInput.telegramBot.sendMessage(chat_id=primitiveInput.telegramChatID, text= primitiveInput.formattedResult)
            #     else:
            #         pass
    elif telegramText == '/stop':
        primitiveInput.Flag = False
    return 'ok'

@primitiveInput.flaskApp.route('/setwebhook', methods = ['GET', 'POST'])
def setwebhook():
    webhook = primitiveInput.telegramBot.setWebhook(f'{primitiveInput.herokuApp}{primitiveInput.telegramToken}')
    if webhook:
        return f'webhook setup successful'
    else:
        return 'webhook setup failed'

@primitiveInput.flaskApp.route('/', methods = ['GET'])
def index():
    return '.'

if __name__ == '__main__':
    database.createDB(primitiveInput)
    primitiveInput.Flag = False
    primitiveInput.flaskApp.run(threaded = True)