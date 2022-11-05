#!/usr/bin/python

# A simple script to copy pokemon from retail carts to a computer via GTS.
# Heavily relies on the sendpkm script and the description of the GTS protocol
# from http://projectpokemon.org/wiki/GTS_protocol
#
# --Infinite Recursion

from pokehaxlib import *
from pkmlib import decode
from base64 import b64decode, b64encode
from binascii import hexlify
from array import array
from http_helper import http_post, notify_gts_service


def makepkm(bytes):
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
        "details": "Pokemon transferred to GTS"
    }"""  % transfer_status

    notify_gts_service("transfer status", status, notify_transfer_url)


def nds_to_gts(create_pkm_url, notify_transfer_url):
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
            decrypt = makepkm(bytes)

            try:
                http_post(
                    url=create_pkm_url,
                    post_data=str(b64encode(decrypt)))
            except Exception as e:
                notify_transfer_with_transfer_status(notify_transfer_url, "error")

            notify_transfer_with_transfer_status(notify_transfer_url, "success")

            sent = True

            break
