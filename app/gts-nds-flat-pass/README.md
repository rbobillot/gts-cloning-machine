# GTS-NDS-FLAT-PASS
---

Simple HTTP server, to be used as DNS for the NSD-CWF

It should simply interact with:
 - the NDS (receive/send binary data)
 - the gts-service (receive/send data (json ? unchanged binary ?))

---
### Known Errors:
```
####################

Unhandled exception in thread started by <function getpkm at 0x1104a97d0>
Traceback (most recent call last):
  File "/Users/rbobillot/gts-cloning-machine/app/gts-nds-flat-pass/src/getpkm.py", line 92, in getpkm
    sock, req = getReq()
  File "/Users/rbobillot/gts-cloning-machine/app/gts-nds-flat-pass/src/pokehaxlib.py", line 146, in getReq
    ans = Request(data)
  File "/Users/rbobillot/gts-cloning-machine/app/gts-nds-flat-pass/src/pokehaxlib.py", line 15, in __init__
    raise TypeError("Not a DS header!")
TypeError: Not a DS header

Context:
 - nds to gts
 - good internet connection
 - bad internet connection

Fix:
 - relaunch flatpass

####################

infinite wait on some request (with slow internet)
  -> should add timeout

####################

NDS/GTS ERROR:

Aucun point d'acces compatible
ne se trouve a proximite. Veuillez
verifier vos parametres de
connexion et ressayer.

Pour toute assistance, visitez
le site www.nintendowifi.com.

- (51099)
  - error: nds is not connected to hotspot
  - fix: retry connection, within nintendo cwf
- (52102)
  - error: nds cannot reach to fake gts
  - fix:
    - check if fake gts is running
    - check if computer is connected to same hotspot than nds
    - restart fake gt if necessary

Global fix: restart flatpass, and get out/in GTS with NDS

####################

Blue screen (HGSS), before receiving Pokemon

Fix:
 - HG: restart flatpass, and retry
 - SS: seems to be buggy, no solution yet

####################

Blue screen (HGSS), after receiving Pokemon

Fix: no action needed

####################