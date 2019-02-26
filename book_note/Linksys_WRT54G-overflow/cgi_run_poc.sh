#!/bin/bash
# cgi_run.sh
# sudo ./cgi_run.sh

DEBUG=$1

LEN=$(echo $DEBUG | wc -c)
PORT="1234"


#if [ "$LEN" == "0" ] || [ "$INPUT" == "-h" ] || [ "$UID" != "0" ]
#then
#    echo -e "\nusage: sudo $0\n"
#    exit 1
#fi

cp $(which qemu-mipsel-static) ./qemu

if [ "$LEN" -eq 1 ]
then 
    echo "EXECUTE MODE\n"
    sudo chroot . ./qemu -E LD_PRELOAD="/libnvram-faker.so" ./usr/sbin/httpd
else
    echo "DEBUG MODE\n"
    sudo chroot . ./qemu -E LD_PRELOAD="/libnvram-faker.so" -g 1234 ./usr/sbin/httpd
fi
echo "run ok"
rm -f ./qemu
