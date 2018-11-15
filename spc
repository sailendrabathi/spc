#!/bin/bash

if [ $# -eq 1 ] 
then
	if [ $1 == "signup" ] || [ $1 == "login" ] || [ $1 == "upload_file" ] || [ $1 == "set_url" ] || [ $1 == "logout" ] || [ $1 == "upload_folder" ] || [ $1 == "delete_file" ] || [ $1 == "delete_folder" ] || [ $1 == "sync" ] || [ $1 == "show_data" ] || [ $1 == "config" ] 
	then 
		python3 linuxclient.py "--"$@
	elif [ $1 == "observe" ] || [ $1 == "version" ] || [ $1 == "server" ] || [ $1 == "info" ]; then
		python3 linuxclient.py "--"$@	
	elif [ $1 == "download_file" ] || [ $1 == "download_folder" ]; then
		python3 linuxclient.py "--"$@
	else
		echo "invalid argument, use 'spc help' command for help"
	fi
elif [ $# -eq 2 ]; then
	if [ $1 == "en-de" ]
	then
		python3 linuxclient.py "--"$1 "--"$2
	else
		echo "invalid arguments, use 'spc help' command for help"
	fi						
else
	echo "invalid number of arguments, use 'spc help' command for help"
fi	