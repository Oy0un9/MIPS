#!/bin/bash
# cgi_run.sh
# sudo ./cgi_run.sh  'uid=1234'  `python  -c "print 'uid='+'A'*600"`

INPUT="$1"
TEST="$2"
LEN=$(echo -n "$INPUT" | wc -c)
PORT="1234"
echo "come on"
if [ "$LEN" == "0" ] || [ "$INPUT" == "-h" ] || [ "$UID" != "0" ]
then
    echo -e "\nusage: sudo $0\n"
    exit 1
fi

cp $(which qemu-mipsel-static) ./qemu

echo "$INPUT"  | chroot .  ./qemu  -E CONTENT_LENGTH=$LEN -E CONTENT_TYPE="application/x-www-form-urlencodede" -E REQUEST_METHOD="POST" -E HTTP_COOKIE=$TEST -E REQUEST_URI="/hedwig.cgi" -E REMOTE_ADDR="192.168.1.1" -g $PORT /htdocs/web/hedwig.cgi #2>/dev/null
echo "run ok"
#rm -f ./qemu
