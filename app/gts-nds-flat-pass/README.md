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

infinite wait on some request
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

Traceback (most recent call last):
  File "/home/rbobillot/Perso/gts-cloning-machine/app/gts-nds-flat-pass/src/getpkm.py", line 118, in getpkm
    post_data=str(b64encode(decrypt)))
  File "/home/rbobillot/Perso/gts-cloning-machine/app/gts-nds-flat-pass/src/getpkm.py", line 81, in http_post
    response = urllib2.urlopen(req)
  File "/usr/lib/python2.7/urllib2.py", line 154, in urlopen
    return opener.open(url, data, timeout)
  File "/usr/lib/python2.7/urllib2.py", line 435, in open
    response = meth(req, response)
  File "/usr/lib/python2.7/urllib2.py", line 548, in http_response
    'http', request, response, code, msg, hdrs)
  File "/usr/lib/python2.7/urllib2.py", line 467, in error
    result = self._call_chain(*args)
  File "/usr/lib/python2.7/urllib2.py", line 407, in _call_chain
    result = func(*args)
  File "/usr/lib/python2.7/urllib2.py", line 633, in http_error_302
    new = self.redirect_request(req, fp, code, msg, headers, newurl)
  File "/usr/lib/python2.7/urllib2.py", line 594, in redirect_request
    raise HTTPError(req.get_full_url(), code, msg, headers, fp)
urllib2.HTTPError: HTTP Error 307: Temporary Redirect

-> Catch any unhandled error, add an error code/message for every of them

####################

Enters GTS before "start transfer"

Cause: probably due to multiple "start transfer" clicks

Solution: restart flatpass

####################

Blue screen (HGSS), before receiving Pokemon

Fix:
 - HG: restart flatpass, and retry
 - SS: seems to be buggy, no solution yet

####################

Blue screen (HGSS), after receiving Pokemon

Fix: no action needed

####################

GET /pokemondpds/worldexchange/info.asp?pid=108015551 HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close


GET /pokemondpds/worldexchange/info.asp?hash=a46ead29d18d9550f7d49634b022067930397be1&pid=108015551&data=SjsteUvNfut= HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close


Connection Established.
GET /pokemondpds/worldexchange/result.asp?pid=108015551 HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close


GET /pokemondpds/worldexchange/result.asp?hash=a46ead29d18d9550f7d49634b022067930397be1&pid=108015551&data=SjsteUvNfut= HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close


GET /pokemondpds/worldexchange/delete.asp?pid=108015551 HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close


GET /pokemondpds/None? HTTP/1.1
Host: gamestats2.gs.nintendowifi.net
User-Agent: GameSpyHTTP/1.0
Connection: close

####################

