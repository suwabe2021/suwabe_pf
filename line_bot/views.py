from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from utils import message_creater
from line_bot.line_message import LineMessage

@csrf_exempt
def index(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        data = request['events'][0]
        message = data['message']
        reply_token = data['replyToken']

        #スタンプが入力されるとKeyErrorになってしまうので回避
        #line_message.py側でも「'文字列以外を入力されると～'」になっている場合の処理を入れる
        try:
            line_message = LineMessage(message_creater.create_single_text_message(message['text']))
        except KeyError:
            line_message = LineMessage( [
                {
                    'type': 'text',
                    'text': '文字列以外を入力されると処理できません。文章で質問してください'
                } ])
 
        line_message.reply(reply_token)
        return HttpResponse("ok")