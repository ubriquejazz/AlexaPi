#!/bin/bash
clear
echo "Press CTRL-Z to quit"
for ip in 192.168.100.{1..255};
do
	ping $ip -c 2&> /dev/null;
	if [ $? -eq 0 ];
	then
		echo $ip is alive
	fi
done
