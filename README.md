# askGPT
LINEからChatGPTへ質問でき、生成AIの良さを体感できるアプリになるよう努めました。

# 制作の経緯
プログラミング学習に際してChatGPTを使う機会が増え、その便利さを実感しました。

しかし、家族に勧めても機械全般に苦手意識があり、「よくわからないから」と使用に消極的でした。

であれば、普段から使っているLINEでChatGPTを使えたなら、利用への敷居が下がるかと思い制作しました。

面倒な手順なく使用開始できるようにしております。

# 環境
* Python 3.12.3
* Django 5.1.4
* langchain_core 0.3.33
* langchain_openai 0.3.3
  
* WEBサーバー:awsのt2.micro
* アプリサーバー:同上


# Usage
https://suwabe2021.ddns.net/login/wodalplchu958guchud/

上記にアクセスして表示されるLINEのQRコードを読み取り友だち追加をしてください。

その後、LINEで追加したアカウントへ質問を投げればChatGPTから返答があります。

※質問の連投はサーバーが落ちる恐れがあるためご遠慮ください。

※10秒程度で返答がなければサーバーが落ちております。

 
# プロジェクトの構成
 
* account:URLから取得した値が一致していればQRコードが表示される仕様。今後の機能拡張用にカスタムユーザー下書き
* askGPT:プロジェクトのメイン
* chatgpt:line_botからのメッセージをChatGPTへ投げ、返答をline_botに返す
* line_bot:LINEへのメッセージ受け渡し、chatgptアプリへのLINEメッセージ受け渡し

 
# 仕様
 
1.友だち追加したアカウントへの投稿はhttps://suwabe2021.ddns.net/line_bot/ へ送信

2.urls.pyをたどりline_bot/views.pyが投稿を受取

3.受信した投稿はjson形式なので、必要なメッセージだけ抜いてlinemessage.pyへ引き渡し

4.class LineMessageでchatgpt/gpt.pyへメッセージを引き渡し

5.sentgpt関数でChatGPTへメッセージの受け渡し。LINEで長文は読みづらいので簡潔な返答をするように指示

6.line_bot/views.pyでメッセージはlinemessage.pyのclass LineMessage内reply関数へ渡されてLINEへ返信される

※LINEスタンプは不正な文字列としてchatGPTに渡されてしまうので、
line_bot/views.pyでKeyErrorを拾いメッセージをユーザー向けのエラー文に差し替える仕様

# Author
 
* 諏訪部貫太
* suwabe2021@gmail.com
