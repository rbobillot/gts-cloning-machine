#!/usr/bin/python

from src.pokehaxlib import *
from src.pkmlib import encode
from src.boxtoparty import makeparty
from src.gbatonds import makends
from sys import argv, exit
from platform import system
import os.path


def sendpkm():
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

    print('Note: you must exit the GTS before sending a pkm')
    print('Enter the path or drag the pkm file here')

    path = input().strip()
    path = os.path.normpath(path)
    if system() != 'Windows':
        path = path.replace('\\', '')

    if path.lower().endswith('.pkm'):
        with open(path, 'rb') as f:
            pkm = f.read()

        # Adding extra 100 bytes of party data
        if len(pkm) != 236 and len(pkm) != 136:
            print('Invalid filesize.')
            return
        if len(pkm) == 136:
            print('PC-Boxed Pokemon! Adding party data...')
            pkm = makeparty(pkm)
            print('done.')

        print('Encoding!')
        bin = encode(pkm)
    elif path.lower().endswith('.3gpkm'):
        print('Converting GBA file to NDS format...')
        with open(path, 'rb') as f:
            pkm = f.read()

        if len(pkm) != 80 and len(pkm) != 100:
            print('Invalid filesize.')
            return
        pkm = makends(pkm)
        print('done.')

        print('Encoding!')
        bin = encode(pkm)
    else:
        print('Filename must end in .pkm or .3gpkm')
        return

    # Adding GTS data to end of file
    bin += pkm[0x08:0x0a]  # id
    if pkm[0x40] & 0x04:
        bin += '\x03'  # Gender
    else:
        bin += bytes((pkm[0x40] & 0x02) | 0x01)
    bin += bytes(pkm[0x8c])  # Level
    # Requesting bulba, either, any
    bin += bytes('\x01\x00\x03\x00\x00\x00\x00\x00', "utf-8")
    bin += bytes('\x00' * 20, "utf-8")  # Timestamps and PID
    bin += pkm[0x68:0x78]  # OT Name
    bin += pkm[0x0c:0x0e]  # OT ID
    bin += bytes('\xDB\x02', "utf-8")  # Country, City
    # Sprite, Exchanged (?), Version, Lang
    bin += bytes('\x46\x00\x07\x02', "utf-8")

    sent = False
    delete = False
    print('Ready to send; you can now enter the GTS...')
    while not sent:
        sock, req = getReq()
        print(req)
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, token)
        elif a == 'info':
            sendResp(sock, '\x01\x00')
            print('Connection Established.')
        elif a == 'setProfile':
            sendResp(sock, '\x00' * 8)
        elif a == 'post':
            sendResp(sock, '\x0c\x00')
        elif a == 'search':
            sendResp(sock, '')
        elif a == 'result':
            sendResp(sock, bin)
        elif a == 'delete':
            sendResp(sock, '\x01\x00')
            sent = True

    print('Pokemon sent successfully.')
