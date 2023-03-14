#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import socket
import httplib
import sys

def sendRequest(host, port, request):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(2.)
    hp = "%s:%d" % (host, port)
    h = httplib.HTTP(hp)
    try:
        h.connect()
    except:
        socket.setdefaulttimeout(old_timeout)
        return 1
    h.putrequest("GET", request)
    h.endheaders()
    errcode, errmsg, headers = h.getreply()
    if errcode != 200:
        socket.setdefaulttimeout(old_timeout)
        return 1
    else:
        socket.setdefaulttimeout(old_timeout)
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = eval(sys.argv[2])
    except:
        sys.exit(1)
    request = sys.argv[3]
    ret = sendRequest(host, port, request)
    sys.exit(ret)
