#LINEでWEBサイトにログインする方法を導入しようとしたが、うまく動作しなかった。
#LINEからのjsonを受け取れておらず、ユーザーが作成されていないのが原因。要調査
#viws.py
"""
from django.shortcuts import render, redirect
import requests
from django.views import View
from django.conf import settings
from django.middleware.csrf import get_token
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from . import forms

User = get_user_model()

#LINEログインに必要な情報を読み込む
SOCIAL_AUTH_LINE_KEY = settings.SOCIAL_AUTH_LINE_KEY
SOCIAL_AUTH_LINE_SECRET = settings.SOCIAL_AUTH_LINE_SECRET
LINE_REDIRECT_URL = settings.LINE_REDIRECT_URL
REDIRECT_KEY = settings.REDIRECT_KEY


# 共通処理関数(IndexView,Authentication)
def render_with_context(request, passwd):
    user_form = forms.UserCreationForm(request.POST or None)

    if request.method == "POST" and user_form.is_valid():
        user = user_form.save(commit=True)
        login(request, user)
        return redirect("main_page/index") #正常に登録されたら
    
    context = {
        "passwd": passwd,
        "truepass": REDIRECT_KEY,
        'user_form': user_form
    }
    return render(request, "account/index.html", context)


#ドメイン/新規登録ページ/のあとにパラメータがない場合
class IndexView(View):
    def get(self, request, passwd=0):
        return render_with_context(request, passwd)

"""
"""
ドメイン/新規登録ページ/passwdの形式でパラメータを受取り、htmlに渡す
新規登録ページ/index.htmlにはパラメータが指定と一致していれば新規登録を表示する処理を記述
"""
"""

class Authentication(View):
    def get(self, request, passwd):
        return render_with_context(request, passwd)


#LINEログイン処理
def line_login(request):
    try:
        token = get_token(request)
        scope = "profile%20openid"
        BOT_PROMPT = "aggressive"
        initial_amr_display = "lineqr"
        line_login_url = (
            f"https://access.line.me/oauth2/v2.1/authorize?response_type=code"
            f"&client_id={SOCIAL_AUTH_LINE_KEY}"
            f"&redirect_uri={LINE_REDIRECT_URL}"
            f"&state={token}"
            f"&bot_prompt={BOT_PROMPT}"
            f"&initial_amr_display={initial_amr_display}"
            f"&scope={scope}"
        )
        return redirect(line_login_url)
    except Exception as e:
        print(f"Error: {e}")
        return redirect("account:index")


#LINEアクセストークン取得・ユーザー登録処理
def line_token(request):
    try:
        code = request.GET.get("code")
        url = "https://api.line.me/oauth2/v2.1/token"

        # リクエストヘッダ
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # リクエストボディ
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LINE_REDIRECT_URL,
            "client_id": SOCIAL_AUTH_LINE_KEY,
            "client_secret": SOCIAL_AUTH_LINE_SECRET
        }

        # POSTリクエストを送信
        response = requests.post(url, headers=headers, data=data)
        token_json = response.json()

        # エラーハンドリング
        if "error" in token_json:
            print(f"Error: {token_json['error_description']}")
            return redirect("account:index")
        
        access_token = token_json.get("id_token") #スコープにopenidを入れたのでこれが返ってくる

        # ユーザープロファイルの取得
        headers2 = {"Authorization": f"Bearer {access_token}"}
        user_res = requests.get("https://api.line.me/v2/profile", headers=headers2)
        user_prof = user_res.json()

        # ユーザー情報の取得
        verify_url = f"https://api.line.me/oauth2/v2.1/verify?id_token={access_token}&client_id={SOCIAL_AUTH_LINE_KEY}"
        response2 = requests.post(verify_url)
        user_info = response2.json()

        # ユーザーの作成または取得
        username = user_prof.get("displayName", "未設定")
        email = user_info.get("aud")+"@exsample.com"
        password = user_info.get("sub")

        user, created = User.objects.get_or_create(email=email, defaults={"username": username})

        if created:
            user.set_password(password)  # パスワードをハッシュ化して保存
            user.save()

        login(request, user)  # ログイン処理
        return redirect("account:index")

    except Exception as e:
        print(f"Error: {e}")
        return redirect("account:index")


#クラスベースビューのインスタンス化
index = IndexView.as_view()
authentication = Authentication.as_view()

"""