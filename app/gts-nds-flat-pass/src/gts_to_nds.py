#!/usr/bin/python

from base64 import urlsafe_b64encode
import hashlib
from pokehaxlib import *
from pkmlib import encode
from http_helper import notify_gts_service

def gts_to_nds_4(pkm, notify_transfer_url):
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

    print('Note: you must exit the GTS before sending a pkm')

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

def gts_to_nds_5(pkm, notify_transfer_url):       
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'
    salt = 'HZEdGCzcGGLvguqUEKQN'

    # Adding extra 100 bytes of party data
    if len(pkm) != 220 and len(pkm) != 136 and len(pkm) != 236:
        print('Invalid filesize: %d bytes. Needs to be either 136 or 220 bytes.' % len(pkm))
        return
    elif len(pkm) == 236:
        pkm = pkm[0:220] # Truncate to 220 bytes (Gen 4 [0xD4:0xEB] bytes are not useful, they can be truncated to [0xD4:0xEB])

    print('Encoding!')
    bin = encode(pkm)

    # Adding GTS data to end of file
    print('Adding GTS data... ')
    bin += '\x00' * 16
    bin += pkm[0x08:0x0a] # id
    if ord(pkm[0x40]) & 0x04: bin += '\x03' # Gender
    else: bin += chr((ord(pkm[0x40]) & 2) + 1)
    bin += pkm[0x8c] # Level
    bin += '\x01\x00\x03\x00\x00\x00\x00\x00' # Requesting bulba, either, any
    bin += '\xdb\x07\x03\x0a\x00\x00\x00\x00' # Date deposited (10 Mar 2011)
    bin += '\xdb\x07\x03\x16\x01\x30\x00\x00' # Date traded (?)
    bin += pkm[0x00:0x04] # PID
    bin += pkm[0x0c:0x0e] # OT ID
    bin += pkm[0x0e:0x10] # OT Secret ID
    bin += pkm[0x68:0x78] # OT Name
    bin += '\xDB\x02' # Country, City
    bin += '\x46\x01\x15\x02' # Sprite, Exchanged (?), Version, Lang
    bin += '\x01\x00' # Unknown
    print('Done.')

    sent = False
    response = ''

    print('Ready to send; you can now enter the GTS.')
    while not sent:
        sock, req = getReq()
        print(req)
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, token)
            continue
        elif a == 'info':
            response = '\x01\x00'
            print('Connection established.')
        elif a == 'setProfile': response = '\x00' * 8
        elif a == 'post': response = '\x0c\x00'
        elif a == 'search': response = '\x01\x00'
        elif a == 'result': response = bin
        elif a == 'delete':
            response = '\x01\x00'
            sent = True
            status = """{
                "status": "success",
                "transfer_platform": "gts-nds",
                "details": "Pokemon transferred to NDS"
            }"""
            notify_gts_service("transfer status", status, notify_transfer_url)

        m = hashlib.sha1()
        m.update(salt + urlsafe_b64encode(response) + salt)
        response += m.hexdigest()
        sendResp(sock, response)

    print('Pokemon sent successfully.')

def gts_to_nds(gen, pkm, notify_transfer_url):
    gtd = gts_to_nds_4 if gen == 4 else gts_to_nds_5
    gtd(pkm, notify_transfer_url)