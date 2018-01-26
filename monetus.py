from flask import Flask, request
from message_handling import define_response
import os
import json, requests, datetime, simplejson, atexit
from flask import Flask
from datetime import date

app = Flask(__name__)


facebook_key = os.environ['facebook_api']
api_key = os.environ['api_key']

@app.route('/', methods=['GET'])
def handle_verification():
    print ("Handling Verification.")
    if request.args.get('hub.verify_token', '') == api_key:
      print ("Verification successful!")
      return request.args.get('hub.challenge', '')
    else:
      print ("Verification failed!")
      return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():  
    print ("Handling Messages")
    payload = request.get_data()

    for sender, message in messaging_events(payload):
      print ("Incoming from %s: %s " % (sender, message))
      send_message(facebook_key, sender, message)
    return "ok"

def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]

    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        elif "postback" in event and "payload" in event["postback"]:
            yield event["sender"]["id"], set_default_messages(event["postback"]["payload"]).encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(facebook_key, sender, text):
    try:
        usermessage = (text.decode("unicode_escape")).lower()
    except:
        usermessage = 'erro'

    responsemessage = define_response(usermessage)

    send_to_facebook(facebook_key, sender, responsemessage)

def send_to_facebook(token, recipient, text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
          "recipient": {"id": recipient},
          "message": {"text": text}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print (r.text)


def set_default_messages(payload):
    if payload == 'SD':
        return ('sd')
    elif payload == 'S':
        return ('s')
    else:
        return ('ajuda')
        


if __name__ == '__main__':
    app.run()