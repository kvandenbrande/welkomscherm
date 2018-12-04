#-*- coding:utf8;-*-
import socket, urllib2
from telegram import send_telegram

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_public():
    try:
        public = urllib2.urlopen("http://ip.42.pl/raw").read()
    except:
        public = "no public IP"

    return public

IP = get_ip()
PUBLIC = get_public()
HOST = socket.gethostname()

MESSAGE = HOST + ": " +IP + "\n" + PUBLIC

try:
    send_telegram(MESSAGE)
except:
    pass
