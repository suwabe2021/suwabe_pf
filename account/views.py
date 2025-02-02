from django.shortcuts import render
from django.views import View
from django.conf import settings

#LINE BUSINESSで設定したリダイレクトと同じURLを読み込む
REDIRECT_KEY = settings.REDIRECT_KEY

# 共通処理関数(IndexView,Authentication)
def render_with_context(request, passwd):
    context = {
        "passwd": passwd,
        "truepass": REDIRECT_KEY,
    }
    return render(request, "account/index.html", context)


#ドメイン/新規登録ページ/のあとにパラメータがない場合
class IndexView(View):
    def get(self, request, passwd=0):
        return render_with_context(request, passwd)

"""
ドメイン/新規登録ページ/passwdの形式でパラメータを受取り、htmlに渡す
新規登録ページ/index.htmlにはパラメータが指定と一致していればLINE QRコードを表示する処理を記述
"""

class Authentication(View):
    def get(self, request, passwd):
        return render_with_context(request, passwd)


#クラスベースビューのインスタンス化
index = IndexView.as_view()
authentication = Authentication.as_view()