#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from time import time
from platform import uname
from datetime import datetime
from psutil import boot_time, \
    cpu_freq, cpu_count, cpu_percent, \
    virtual_memory, swap_memory, \
    disk_partitions, disk_usage

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to get information about the system.
"""

# Get size
def get_size(bolter, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bolter < factor:
            return f"{bolter:.2f}{unit}{suffix}"

        bolter /= factor

""" Get system info """
def SystemInfo() -> str:
    info = uname()
    return (f"""
System {repr(info.system)}
Node Name {repr(info.node)}
Release {repr(info.release)}
Version {repr(info.version)}
Machine {repr(info.machine)}
Processor {repr(info.processor)}
    """)

""" Get processor info """
def GetCpuInfo() -> str:
    cpufreq = cpu_freq()
    return (f"""
Physical Cores {cpu_count(logical=False)}
Total Cores {cpu_count(logical=True)}
Max Frequency {cpufreq.max:.2f}Mhz
Min Frequency {cpufreq.min:.2f}Mhz
Current Frequency {cpufreq.current:.2f}Mhz
CPU Usage {cpu_percent()}%"
    """)

""" Get RAM info """
def GetRamInfo() -> str:
    swap = swap_memory()
    svmem = virtual_memory()
    return (f"""
Total Mem {get_size(svmem.total)}
Available Mem {get_size(svmem.available)}
Used Mem {get_size(svmem.used)}
Percentage {get_size(svmem.percent)}%

Total Swap {get_size(swap.total)}
Free Swap {get_size(swap.free)}
Used Swap {get_size(swap.used)}
Percentage Swap {get_size(swap.percent)}%
    """)

""" Get disk info """
def GetDiskInfo() -> str:
    data = ""
    for partition in disk_partitions():
        data += f"\n\tDevice {partition.device}\n\tMountpoint {partition.mountpoint}\n\tFile System {partition.fstype}"
        try:
            usage = disk_usage(partition.mountpoint)
            total = get_size(usage.total)
            used = get_size(usage.used)
            free = get_size(usage.free)
            percent = get_size(usage.percent)
        except PermissionError:
            data += "\n\n"
            continue
        else:
            data += f"\n\tTotal Size {total}\n\tUsed {used}\n\tFree {free}\n\tPercentage {percent}\n\t"

    return data

""" Get system boot time in seconds """
def GetBootTime() -> str:
    boot = boot_time()
    ago = int(time() - boot)
    bt = datetime.fromtimestamp(boot)
    return f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second} ({ago} seconds ago)"

""" Handle telegram command """
def Handle(callback: dict, bot) -> None:
    chatid = callback.from_user.id
    action = callback.data.split('_')[-1]

    bot.send_chat_action(chatid, "typing")

    if action == "RAM":
        result = GetRamInfo()
    elif action == "BOOT":
        result = GetBootTime()
    elif action == "DISK":
        result = GetDiskInfo()
    elif action == "SYS":
        result = SystemInfo()
    elif action == "CPU":
        result = GetCpuInfo()
    else:
        result = "No data"

    bot.send_message(chatid, result)
