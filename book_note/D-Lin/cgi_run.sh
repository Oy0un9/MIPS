#!/bin/bash
# cgi_run.sh
# sudo ./cgi_run.sh `

python generate.py
INPUT=$(<payload)

LEN=$(echo $INPUT | wc -c)
PORT="1234"


if [ "$LEN" == "0" ] || [ "$INPUT" == "-h" ] || [ "$UID" != "0" ]
then
    echo -e "\nusage: sudo $0\n"
    exit 1
fi

cp $(which qemu-mipsel-static) ./qemu

echo "$INPUT"  | chroot .  ./qemu  -E CONTENT_LENGTH=$LEN -E CONTENT_TYPE="application/x-www-form-urlencodede" -E REQUEST_METHOD="POST"  -E REQUEST_URI="/authentication.cgi" -E REMOTE_ADDR="192.168.1.1" -g $PORT /htdocs/web/authentication.cgi 2>/dev/null
rm -f ./qemu

