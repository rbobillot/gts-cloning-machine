#!/usr/bin/python

# A simple script to copy pokemon from retail carts to a computer via GTS.
# Heavily relies on the sendpkm script and the description of the GTS protocol
# from http://projectpokemon.org/wiki/GTS_protocol
#
# --Infinite Recursion

import hashlib
from pokehaxlib import *
from pkmlib import decode
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
from binascii import hexlify
from array import array
from http_helper import http_post, notify_gts_service


def makepkm_4(bytes):
    ar = array('B')  # Byte array to hold encrypted data
    ar.fromstring(bytes)

    # checksum is first four bytes of data, xor'd with 0x4a3b2c1d
    chksm = (eval('0x' + hexlify(ar[0:4]))) ^ 0x4a3b2c1d

    bin = ar[4:len(ar)]  # Byte array for decrypt operations
    pkm = array('B')    # ...and one for the output file

    # Running decryption algorithm
    GRNG = chksm | (chksm << 16)
    for i in range(len(bin)):
        GRNG = (GRNG * 0x45 + 0x1111) & 0x7fffffff
        keybyte = (GRNG >> 16) & 0xff
        pkm.append((bin[i] ^ keybyte) & 0xff)

    pkm = pkm[4:len(pkm)]
    pkm = pkm[0:236].tostring()
    pkm = decode(pkm)

    return pkm


def notify_transfer_with_transfer_status(notify_transfer_url, transfer_status):
    status = """{
        "status": "%s",
        "transfer_platform": "nds-gts",
        "details": "Transfering Pokemon to GTS"
    }"""  % transfer_status

    notify_gts_service("transfer status", status, notify_transfer_url)


def nds_to_gts_4(create_pkm_url, notify_transfer_url):
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'
    sent = False

    print('Ready to receive from NDS')

    while not sent:
        sock, req = getReq()
        a = req.action

        if len(req.getvars) == 1:
            sendResp(sock, token)
        elif a == 'info':
            sendResp(sock, '\x01\x00')
            print('Connection Established.')
        elif a == 'setProfile':
            sendResp(sock, '\x00' * 8)
        elif a == 'result':
            sendResp(sock, '\x05\x00')
        elif a == 'delete':
            sendResp(sock, '\x01\x00')
        elif a == 'search':
            sendResp(sock, '')
        elif a == 'post':
            sendResp(sock, '\x0c\x00')
            print('Receiving Pokemon...')
            data = req.getvars['data']
            bytes = b64decode(data.replace('-', '+').replace('_', '/'))
            decrypt = makepkm_4(bytes)

            try:
                http_post(
                    url=create_pkm_url,
                    post_data=str(b64encode(decrypt)))
                print('Pokemon sent to GTS !')
            except Exception as e:
                notify_transfer_with_transfer_status(notify_transfer_url, "error")

            notify_transfer_with_transfer_status(notify_transfer_url, "success")

            sent = True

            break

def makepkm_5(bytes):
    ar = array('B') # Byte array to hold encrypted data
    ar.fromstring(bytes)

    ar = ar[12:232].tostring()
    pkm = decode(ar)

    return pkm

def nds_to_gts_5(create_pkm_url, notify_transfer_url):
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'
    salt = 'HZEdGCzcGGLvguqUEKQN'
    sent = False
    response = ''
    print('Ready to receive from game.')
    while not sent:
        sock, req = getReq()
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, token)
            continue
        elif a == 'info':
            response = '\x01\x00'
            print('Connection Established.')
        elif a == 'setProfile': response = '\x00' * 8
        elif a == 'result': response = '\x05\x00'
        elif a == 'delete': response = '\x01\x00'
        elif a == 'search': response = '\x01\x00'
        elif a == 'post':
            response = '\x0c\x00'
            print('Receiving Pokemon...')
            data = req.getvars['data']
            bytes = urlsafe_b64decode(data)
            decrypt = makepkm_5(bytes)
            try:
                http_post(
                    url=create_pkm_url,
                    post_data=str(b64encode(decrypt)))
                print('Pokemon sent to GTS !')
            except Exception as e:
                print(e)
                notify_transfer_with_transfer_status(notify_transfer_url, "error")

            notify_transfer_with_transfer_status(notify_transfer_url, "success")
            sent = True

        m = hashlib.sha1()
        m.update(salt + urlsafe_b64encode(response) + salt)
        response += m.hexdigest()
        sendResp(sock, response)

def nds_to_gts(gen, create_pkm_url, notify_transfer_url):
    ntg = nds_to_gts_4 if gen == 4 else nds_to_gts_5
    ntg(create_pkm_url, notify_transfer_url)