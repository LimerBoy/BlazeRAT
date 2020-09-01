#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from time import ctime
from os import path, mkdir
from services.startup import CURRENT_DIRECTORY

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to record
    all actions of all users.
"""

LOG_DIR = path.join(CURRENT_DIRECTORY, "logs")

# Create logs dir if not exists
if not path.exists(LOG_DIR):
    mkdir(LOG_DIR)

""" Log text to file """
def Log(text: str, chatid: int) -> None:
    text = f"{ctime()} - {text}"
    file = path.join(LOG_DIR, str(chatid) + ".log")
    print(text)
    with open(file, "a") as log_file:
        log_file.write(text + "\n")
