import socket
import sys
import time
import thread

class Request:
    def __init__(self, h=None):
        _gen_4_base_route = '/pokemondpds'
        _gen_5_base_route = '/syachi2ds/web'

        if not h:
            self.action = None
            self.page = None
            self.getvars = {}
            self.base_route = ''
            self.gen = -1
            return

        if not h.startswith("GET"):
            raise TypeError("Not a DS header !", h)

        if _gen_4_base_route in h:
            self.base_route = _gen_4_base_route
            self.gen = 4
        elif _gen_5_base_route in h:
            self.base_route = _gen_5_base_route
            self.gen = 5
        else:
            raise TypeError("Not a gen 4 nor 5 DS header !", h)

        def get_target_url(head):
            """
            Base requests are formatted like this:
            # Gen 4: 'GET /pokemondpds/worldexchange/info.asp?pid=108015551 HTTP/1.1\r\nHost: gamestats2.gs.nintendowifi.net\r\nUser-Agent: GameSpyHTTP/1.0\r\nConnection: close\r\n\r\n'
            # Gen 5: 'GET /syachi2ds/web/worldexchange/info.asp?pid=601749232 HTTP/1.1\r\nHost: gamestats2.gs.nintendowifi.net\r\nUser-Agent: GameSpyHTTP/1.0\r\nConnection: close\r\n\r\n'

            We need to extract the target URL: 'worldexchange/info.asp?pid=108015551'
            - info.asp: the action
            - pid: the ID of the DS Cartridge
            """
            target_endpoint = "%s/" % self.base_route
            target_url_index = head.find(target_endpoint) + len(target_endpoint)
            http_version_index = head.find("HTTP/1.1") - 1
            return head[target_url_index:http_version_index]

        request = get_target_url(h)
        query_params_index = request.find("?")
        query_params = request[query_params_index + 1:].split("&")
        vars = dict((i[:i.find("=")], i[i.find("=")+1:]) for i in query_params)

        self.page = request[:query_params_index]
        self.action = request[request.find("/")+1:request.find(".asp?")]
        self.getvars = vars

    def __str__(self):
        if self.page == None:
            raise TypeError("No target endpoint !", self)
        request = "%s?%s" % (self.page, '&'.join("%s=%s" % i for i in self.getvars.items()))
        return 'GET %s/%s HTTP/1.1\r\n' % (self.base_route, request) + \
            'Host: gamestats2.gs.nintendowifi.net\r\nUser-Agent: GameSpyHTTP/1.0\r\n' + \
            'Connection: close\r\n\r\n'

    def __repr__(self):
        return "<Request for %s, with %s>" % (self.action, ", ".join(i+"="+j for i, j in self.getvars.items()))


class Response:
    pokes = None
    resps = None

    def __init__(self, h):
        self.data = h

    def __str__(self):
        months = ["???", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        t = time.gmtime()
        return "HTTP/1.1 200 OK\r\n" + \
               "Date: %s, %02i %s %i %02i:%02i:%02i GMT\r\n" % (days[t[6]], t[2], months[t[1]], t[0], t[3], t[4], t[5]) + \
               "Server: Microsoft-IIS/6.0\r\n" + \
               "P3P: CP='NOI ADMa OUR STP'\r\n" + \
               "cluster-server: aphexweb3\r\n" + \
               "X-Server-Name: AW4\r\n" + \
               "X-Powered-By: ASP.NET\r\n" + \
               "Content-Length: %i\r\n" % len(self.data) + \
               "Content-Type: text/html\r\n" + \
               "Set-Cookie: ASPSESSIONIDQCDBDDQS=JFDOAMPAGACBDMLNLFBCCNCI; path=/\r\n" + \
               "Cache-control: private\r\n\r\n" + self.data

    def getpkm(self):
        all = []
        data = self.data
        while data:
            result = data[:292]
            data = data[292:]
            all.append(result[:136])
        return all


def dnsspoof():
    dns_server = "178.62.43.212"  # This is the unofficial pkmnclassic.net server
    s = socket.socket()
    s.connect((dns_server, 53))
    spoof_addr = s.getsockname()[0]
    me = "".join(chr(int(x)) for x in spoof_addr.split("."))
    print("Please set your DS's DNS server to %s" % spoof_addr)

    """
    Save the spoof_dns_addr to a file,
    so it can be shared through the networks and requested by the clients
    """
    f = open("spoof_addr.txt", "w")
    f.write(spoof_addr)
    f.close()

    dnsserv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dnsserv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    dnsserv.bind(("0.0.0.0", 53))
    while True:
        r = dnsserv.recvfrom(512)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((dns_server, 53))
        s.send(r[0])
        rr = s.recv(512)
        if "gamestats2" in rr:
            rr = rr[:-4]+me
        dnsserv.sendto(rr, r[1])
        # TODO: handle nds connection status
        # print('NDS Connected', r[1])


serv = None


def initServ():
    global serv
    thread.start_new_thread(dnsspoof, ())
    serv = socket.socket()
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(("0.0.0.0", 80))
    serv.listen(5)


def getReq():
    global serv
    sock, addr = serv.accept()
    sock.settimeout(2)
    data = ""
    while True:
        try:
            a = sock.recv(500)
            data += a
        except socket.timeout:
            break
    ans = Request(data)
    return sock, ans


def sendResp(sock, data):
    global serv
    resp = Response(data) if not isinstance(data, Response) else data
    sock.send(str(resp))
    sock.shutdown(2)
    return


def respFromServ(req):
    s = socket.socket()
    s.connect(("178.62.43.212", 80))
    s.send(str(req))
    data = ""
    while True:
        a = s.recv(500)
        if not a:
            break
        data += a
    return Response(data)


def serverResp():
    sock, req = getReq()
    resp = respFromServ(req)
    sendResp(sock, resp)
