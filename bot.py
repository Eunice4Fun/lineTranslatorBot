import logging
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from openai_translator import translate_to_english

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_SECRETS"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text
    logging.info(f'{user_id}: {text}')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translate_to_english(text))
    )


if __name__ == "__main__":
    app.run(debug=True)
