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
    if text == '날씨':
      inbound_message = forecast()
    else:
      inbound_message = username + " in " + channel_name + " says: " + text
    send_message(channel_id, unicode("따라쟁이 놀이 ", 'utf-8') + " " + inbound_message)
    print(inbound_message)
  return Response(), 200

def forecast():
  api_key = "f0ad1b95c9fc6c9d0635c5b8a99f0b06"
  lat = -31.967819
  lng = 115.87718

  forecast = forecastio.load_forecast(api_key, lat, lng)
  byHour = forecast.hourly()
  print byHour.summary
  
  send_message(channel_id, unicode("내일날씨는 ", 'utf-8') + " " + inbound_message)
  return byHour.summary

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True)
