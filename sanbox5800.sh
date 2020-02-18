#!/bin/bash
snmpget -c public -v 1 $1 $2|tr -s " "|cut -f 4- -d " "|tr -d " "
