from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import chat_completion
import threading  # バックグラウンド処理用のスレッドライブラリ

app = Flask(__name__)

configuration = Configuration(access_token='YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 非同期に実行されるバックグラウンドタスク用の関数
def process_and_reply_async(reply_token, user_message):
    try:
        # 重い処理（Gemini APIの呼び出し。通常数秒かかる）
        text = chat_completion.call(user_message)

        # LINEプラットフォームへ応答メッセージを送信
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
    except Exception as e:
        app.logger.error(f"Error in background task: {e}")


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # スレッドセーフにデータを渡すため、スレッド起動前に必要な値をコピーしておく
    reply_token = event.reply_token
    user_message = event.message.text

    # バックグラウンド処理を行うスレッドを起動
    task_thread = threading.Thread(
        target=process_and_reply_async,
        args=(reply_token, user_message)
    )
    task_thread.start()
    # メインスレッドは即座に終了し、Webhookの呼び出し元（LINE側）に瞬時に 200 OK を返す


if __name__ == "__main__":
    app.run(port=15000)
