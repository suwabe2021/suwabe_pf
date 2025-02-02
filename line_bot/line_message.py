from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from chatgpt.gpt import sentgpt
import json
from django.conf import settings

ACCESSTOKEN = settings.ACCESSTOKEN

REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

class LineMessage():
    def __init__(self, messages):
        if messages[0]['text'] == "文字列以外を入力されると処理できません。文章で質問してください":
            self.messages = messages
        else:
            self.messages = [
                {**message, 'text': sentgpt(message['text'])} 
                for message in messages
                ]

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
        }
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)