from flask import Flask, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (InvalidSignatureError)
import sqlite3


app = Flask(__name__)


@app.route("/")
def index():
    return 'line bot ran v2'


line_bot_api = LineBotApi('239Nfdlzdog9Sxgv/+wgktJPT1Qv9v5Y2oYgVcZkyefEUqqZP5glXKEneFJx+NbH3igLmfjYzssPoaNnzIOAc2lGQcPpx04VRMqSb7qF9MqbnLlpp6vCtHU6aXZ2pGxZwdD+8qHSoi4YhuENXYjG3wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c8b6b3c6cd8160b35da56fe705893ba6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return
        #print("Invalid signature. Please check your channel access token/channel secret.")
        #abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handleMessage(event):

    # get msg in
    message_in = event.message.text
    message_in = message_in.upper()
    print("="*50)
    print("message in = ", message_in)

    # get id line
    user_id_line = event.source
    user_id_line = str(user_id_line)
    print("user id line = ", user_id_line)
    print("="*50)
    
    # send msg
    def msg_out(message_out):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message_out))
        print("-"*50)
        print(message_out)
        print("-"*50)

    # send detail site (Ex. "RAN.NMA0001")
    if message_in[0:4] == "RAN." and len(message_in) == 11:

        site_code = message_in[4:11]

        con = sqlite3.connect("data_site_dtac_ne.db")
        cur = con.cursor()
        sql = 'SELECT * from tb_site_dtac_ne WHERE SiteCode = "{}"'.format(site_code)
        curs = cur.execute(sql)
        data = curs.fetchall()

        # Check result
        if len(data) != 0:
            data = data[0]
            message_out = "Site Code : {}\nSite Name : {}\nLat Long : {}\nTower Owner : {}\nTower Type : {}\nFSO : {}".format(data[0], data[1], data[2], data[3], data[4], data[5])
            msg_out(message_out)
        else:
            msg_out(site_code, "*No Data*")


# run server in terminal #
if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")