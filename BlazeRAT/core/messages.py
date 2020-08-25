#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to store the text and,
    if necessary, quickly translate it into other languages.
"""


""" Authorization messages """
class auth:
    incorrect_token = "⛔️ Incorrect token, attempts left %i"
    user_authorized = "🔑 User %s authorized as '%s',\nsession will expire at %s"
    already_authorized = "⚠️ You are already authorized!"
    not_authorized = "⛔️ Access denied, you need to authorize!"
    permission_not_found = "⚠️ You don't have permissions to do this!"
    user_deauthorized = "☠️ User %s deauthorized"
    user_is_banned = "💣 Account is banned, reason '%s'"

""" Services messages """
class services:
    # Desktop screenshot
    desktop_screenshot_captured = "🌃 Desktop screenshot taken"
    # Webcam screenshot
    webcam_screenshot_captured = "📹 Webcam screenshot taken"
    webcam_screenshot_button = "📹 Take screenshot"
    webcam_start_recording_button = "▶️ Start video recording"
    webcam_stop_recording_button = "⏹ Stop video recording"
    webcam_select_action = "🎥 Select an action...\nDevice index is %i"
    webcam_recording_started = "📸 Webcam recording started"
    webcam_recording_stopped = "📷 Webcam recording stopped"
    webcam_recording_not_started = "📷 Unable to stop recording because it was not started!"
    webcam_recording_not_stopped = "📸 It is impossible to start recording as it is already started!"
    webcam_failed_open = "📷 Failed to open webcam %i"
    # System audio volume control
    volume_get_level_button = "🔉 Current level is %i"
    volume_set_level_button = "🔊 Set %i"
    volume_get_level = "🔉 Current volume level is %i"
    volume_set_level = "🔊 Changed volume level to %i"
    # Micophone recorder
    microphone_start_recording_button = "▶️ Start recording"
    microphone_stop_recording_button = "⏹ Stop recording"
    microphone_select_action = "🎤 Select an action..."
    microphone_recording_started = "🎙 Recording started"
    microphone_recording_stopped = "🎙 Recording stopped"
    microphone_recording_not_started = "🎤 Unable to stop recording because it was not started!"
    microphone_recording_not_stopped = "🎤 It is impossible to start recording as it is already started!"
    # Keylogger controls
    keylogger_start_recording_button = "▶️ Start logger"
    keylogger_stop_recording_button = "⏹ Stop logger"
    keylogger_get_logs_button = "⌨️ Retrieve logs"
    keylogger_clean_logs_button = "♻️️ Clean logs"
    keylogger_logs_received = "📄 Here is keylogger logs"
    keylogger_logs_cleaned = "🚮 Keylogger logs cleaned"
    keylogger_recording_started = "⌨️ Keylogger started"
    keylogger_recording_stopped = "⌨️ Keylogger stopped"
    keylogger_recording_not_started = "⁉️Unable to stop keylogger because it was not started!"
    keylogger_recording_not_stopped = "⁉️It is impossible to start keylogger as it is already started!"
    # Power controls
    power_control = "🔋 Select power command:"
    power_received = "🔋 Power event %s received"
    power_shutdown = "🔻 Shutdown"
    power_suspend = "🔻 Suspend"
    power_reboot = "🔻 Reboot"
    power_logout = "🔻 Log out"
    # Location
    location_success = "🗺 Location:\n\tLatitude: %f\n\tLongitude: %f\n\tRange: %i\n\tAddress: \"%s\"\n\n📡 %s"
    location_gateway_detection_failed = "📡 Failed to get default gateway!"
    location_arp_request_failed = "📡 Failed to get gateway mac address!"
    location_api_request_failed = "📡 Failed to make API request!"
    # Shell commands
    shell_session_opened = "⚙️ Terminal session opened"
    shell_session_closed = "⚙️ Terminal session closed"
    shell_command_is_empty = "🐚 Input command is empty!"
    shell_command_executed = "🐚 System command executed.\n%s"
    shell_pwd_success = "📂 Current directory is:\n%s"
    shell_chdir_success = "📂 Current directory changed to:\n%s"
    shell_chdir_not_found = "📂 Directory not found:\n%s"
    shell_chdir_not_a_dir = "📂 Not a directory:\n%s"
    shell_chdir_failed = "📂 (%s)\nFailed to change directory to:\n%s"
    # Process manager
    taskmanager_process_list = "⚙ Taskmanager (%s) running %i processes:"
    taskmanager_process_kill_success = "🔫 Process %s (%i) killed"
    taskmanager_process_kill_failed = "🔫 Failed to kill process %i, error:\n%s"
    # Wipe browsers data
    wipe_files_count = "🧨 %i files will be deleted beyond recovery"
    wipe_confirm = "♻️ Do you want to clean browsers data?"
    wipe_agree = "✅ Wipe all data"
    wipe_disagree = "🛑 NO!"
    wipe_cancelled = "✅ Wipe cancelled"
    wipe_removed = "🗑 Removed %i files from system"
    # Installation
    stub_install = "👻 Installing service..."
    stub_uninstall = "🗑 Uninstalling service..."


""" File transfer and filemanager """
class file:
    upload_path_not_found = "📄 File %s not found!"
    download_file_success = "📄 File %s saved"
    start_file_success = "📄 Start file:\n%s"
    remove_directory_success = "🗑 Directory removed:\n%s"
    remove_directory_failed = "🗑 (%s)\nFailed to remove directory:\n%s"
    remove_file_success = "🗑 File removed:\n%s"
    remove_file_failed = "🗑 (%s)\nFailed to remove file:\n%s"

""" User messages """
class user:
    name_anonymous = "Anonymous"
    help = ("""
🔑 *[Auth]*
/authorize <token>
/deauthorize
/permissions
🗃 *[Files]*
/download <file/dir>
/filemanager
👁‍🗨 *[Spying]*
/location
/keylogger
/information
/webcam <device>
/screenshot
/microphone
🐚 *[System]*
/taskmanager
/uninstall
/keyboard
/volume
/power
/shell
/wipe
    """)
