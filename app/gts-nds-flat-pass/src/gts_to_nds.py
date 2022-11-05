#!/usr/bin/python

from pokehaxlib import *
from pkmlib import encode
from http_helper import notify_gts_service

def gts_to_nds(pkm, notify_transfer_url):
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

    print('Note: you must exit the GTS before sending a pkm')

    # Adding extra 100 bytes of party data
    if len(pkm) != 236 and len(pkm) != 136:
        print('Invalid pkm.')
        status = {
            "status": "error",
            "transfer_platform": "gts-nds",
            "details": "Pokemon not transferred to NDS (pkm is invalid)"
        }
        notify_gts_service("transfer status", status, notify_transfer_url)
        return

    print('Encoding!')
    bin = encode(pkm)
    print('done.')

    # Adding GTS data to end of file
    bin += pkm[0x08:0x0a]  # id
    if ord(pkm[0x40]) & 0x04:
        bin += '\x03'  # Gender
    else:
        bin += chr((ord(pkm[0x40]) & 2) + 1)
    bin += pkm[0x8c]  # Level
    bin += '\x01\x00\x03\x00\x00\x00\x00\x00'  # Requesting bulba, either, any
    bin += '\x00' * 20  # Timestamps and PID
    bin += pkm[0x68:0x78]  # OT Name
    bin += pkm[0x0c:0x0e]  # OT ID
    bin += '\xDB\x02'  # Country, City
    bin += '\x46\x00\x07\x02'  # Sprite, Exchanged (?), Version, Lang

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
            print('Pokemon sent successfully.')
            sent = True

            status = """{
                "status": "success",
                "transfer_platform": "gts-nds",
                "details": "Pokemon transferred to NDS"
            }"""
            notify_gts_service("transfer status", status, notify_transfer_url)
