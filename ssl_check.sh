#!/bin/sh
platform='uknown'
str="$(uname)"
if [ "$str" == 'Linux' ]; then
    platform='linux'
elif [ "$str" == 'FreeBSD' ]; then
    platform='freebsd'
fi
#echo "$platform"
SERVER=$1
PORT=$2
TIMEOUT=25
RETVAL=0
TIMESTAMP=`echo | date`

if [ -z "$2" ]; then
    PORT=443;
else
    PORT=$2;
fi

EXPIRE_DATE=`echo | openssl s_client -connect $SERVER:$PORT -servername $SERVER 2>/dev/null | openssl x509 -noout -dates 2>/dev/null | grep notAfter | cut -d'=' -f2`
#echo "$EXPIRE_DATE"

if [ "$platform" == 'linux' ]; then
    EXPIRE_SECS=`date -d "$EXPIRE_DATE" +'%s'`
elif [ "$platform" == 'freebsd' ]; then
    EXPIRE_SECS=`date -j -f "%b %d %T %Y %Z" "$EXPIRE_DATE" "+%s"`
fi

#echo "$EXPIRE_SECS"
EXPIRE_TIME=$(( ${EXPIRE_SECS} - `date +%s` ))
#echo "$EXPIRE_TIME"
if test $EXPIRE_TIME -lt 0
then
    RETVAL=0
else
    RETVAL=$(( ${EXPIRE_TIME} / 24 / 3600 ))
fi
 
echo "$TIMESTAMP | $SERVER:$PORT expires in $RETVAL days" >> /usr/lib/zabbix/externalscripts/ssl_check.log
echo ${RETVAL}
