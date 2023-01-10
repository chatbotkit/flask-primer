import os
import requests
from operator import itemgetter
from flask import Flask, render_template

chatbotkit_token = os.getenv('CHATBOTKIT_TOKEN')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    headers = {
        'Authorization': f'Bearer {chatbotkit_token}'
    }

    response01 = requests.post(url = 'https://api.chatbotkit.com/v1/conversation/create', headers=headers, json={
        'backstory': 'This is a friendly chat bot.'
    })

    if not response01.ok:
        message = itemgetter('message')(response01.json())

        raise Exception(message)

    conversationId = itemgetter('id')(response01.json())

    response02 = requests.post(url = f'https://api.chatbotkit.com/v1/conversation/{conversationId}/token/create', headers=headers, json={
        'durationInSeconds': 3600 # 1 hour in seconds
    })

    if not response02.ok:
        message = itemgetter('message')(response02.json())

        raise Exception(message)

    token = itemgetter('token')(response02.json())

    return {
        'conversationId': conversationId,
        'token': token
    }
