import __init__, telegram, os, credentials
from flask import Flask

def main():
    primitiveInput = __init__.main()

    # Defigning base URLS
    primitiveInput.cowinAllStatesURL = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    primitiveInput.cowinAllDistrictsURL = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{primitiveInput.stateID}"
    primitiveInput.cowinSearchByDistrictURL = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={primitiveInput.districtID}&date={primitiveInput.searchDate}'

    # Creating Telegram Bot
    primitiveInput.telegramToken = credentials.TELEGRAM_TOKEN
    primitiveInput.telegramBot = telegram.Bot(token = primitiveInput.telegramToken)
    primitiveInput.telegramChatID = credentials.TELEGRAM_CHAT_ID

    # Creating Heroku App
    primitiveInput.herokuApp = 'https://a5ef161f052e.ngrok.io/'

    # Creating Flask App
    primitiveInput.flaskApp = Flask(__name__)

    # Defigning Database
    os.environ['DATABASE_URL'] = 'postgres://akodgvunalckso:50709e8569ce87c56216fc7cd6f24951c64b6322c4124f1862325f0a01ce2eec@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d6o7alcv0mq3lj'

    # Setting Default Variables

    return primitiveInput
