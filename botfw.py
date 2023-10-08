# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 14:08:49 2023

@author: Nolan
"""
import os
import telebot
from slack_sdk import WebClient

# Tạo client Slack
slacktoken = os.environ["SLACK_BOT_TOKEN"]

# Tạo bot Telegram
bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])

# Danh sách các channel cần forward message
channels = os.environ.get("CHANNELS")

# Channel cần forward message đến
channel =  os.environ.get("MYCHANNEL")

forward_message_is_running = False


listchannel = list(i for i in channels.split(","))

client = WebClient(token=slacktoken)

# Hàm forward message
def forward_message(event):
    # Lấy thông tin message
    channel_id = event["channel"]
    user_id = event["user"]
    text = event["text"]

    # Gửi message đến channel cần forward
    if (forward_message_is_running is True):
        client.chat.postMessage(channel=channel, text=text, channel_id=channel_id, user_id=user_id)
@bot.message_handler(commands=['startbotfw'])
def start_forward(message):
    # Bật hàm forward message
    global forward_message_is_running
    forward_message_is_running = True

    # Gửi thông báo đến người dùng
    bot.send_message(message.chat.id, "Bot forward message đã được khởi động.")

@bot.message_handler(commands=['stopbotfw'])
def stop_forward(message):
    # Tắt hàm forward message
    global forward_message_is_running
    forward_message_is_running = False

    # Gửi thông báo đến người dùng
    bot.send_message(message.chat.id, "Bot forward message đã được dừng.")

# Chạy bot
while True:
    for channel in listchannel:
       client.rtm_connect(on_message=forward_message, channel=channel)
    bot.polling()
