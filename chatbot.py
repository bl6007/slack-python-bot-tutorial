# -*- coding: utf-8 -*- 
import os
import forecastio
from flask import Flask, request, Response
from slackclient import SlackClient

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)

def send_message(channel_id, message):
  slack_client.api_call(
      "chat.postMessage",
      channel=channel_id,
      text=message,
      username='abcdBot',
      icon_emoji=':monkey_face:'
  )

@app.route('/webhook', methods=['POST'])
def inbound():
  username = request.form.get('user_name')
  if request.form.get('token') == SLACK_WEBHOOK_SECRET and username != 'slackbot':
    channel_name = request.form.get('channel_name')
    channel_id = request.form.get('channel_id')
    username = request.form.get('user_name')
    text = request.form.get('text')
    
    if text == unicode("날씨", 'utf-8'):
      inbound_message = forecast()
    else:
      inbound_message = username + " in " + channel_name + " says: " + text
      
    send_message(channel_id, inbound_message)
    print(inbound_message)
  return Response(), 200

def forecast():
  api_key = "f0ad1b95c9fc6c9d0635c5b8a99f0b06"
  lat = 37.5124413
  lng = 126.9540519

  forecast = forecastio.load_forecast(api_key, lat, lng)
  byHour = forecast.hourly()
  return byHour.summary

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True)
