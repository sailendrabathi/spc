#!/bin/bash

if [ $# -eq 1 ] 
then
	if [ $1 == "signup" ] || [ $1 == "login" ] || [ $1 == "upload_file" ] || [ $1 == "set_url" ] || [ $1 == "logout" ] || [ $1 == "upload_folder" ] || [ $1 == "delete_file" ] || [ $1 == "delete_folder" ] || [ $1 == "sync" ] || [ $1 == "show_data" ] || [ $1 == "config" ] 
	then 
		python3 linuxclient.py "--"$@
	elif [ $1 == "observe" ] || [ $1 == "version" ] || [ $1 == "server" ] || [ $1 == "info" ] || [ $1 == "status" ]; then
		python3 linuxclient.py "--"$@	
	elif [ $1 == "download_file" ] || [ $1 == "download_folder" ]; then
		python3 linuxclient.py "--"$@
	else
		echo "invalid argument, use 'spc info' command for help"
	fi
elif [ $# -eq 2 ]; then
	if [ $1 == "en-de" ]; then
		if [ $2 == "list" ] || [ $2 == "update" ]; then 
			python3 linuxclient.py "--"$2
		else
			echo "invalid arguments, use 'spc info' command for help"	
		fi
	else
		echo "invalid arguments, use 'spc info' command for help"
	fi
elif [ $# -eq 3 ]; then
	if [ $1 == "en-de" ] && [ $2 == "update" ]; then
		python3 linuxclient.py "--update1" $3
	elif [ $1 == "en-de" ] && [ $2 == "dump" ]; then
		python3 linuxclient.py "--dump" $3
	else
		echo "invalid arguments, use 'spc info' command for help"
	fi							
else
	echo "invalid number of arguments, use 'spc info' command for help"
fi	