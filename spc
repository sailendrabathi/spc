#!/bin/bash

if [ $# -eq 1 ] 
then
	if [ $1 == "signup" ] || [ $1 == "login" ] || [ $1 == "logout" ]; then
		python3 linuxclient.py "--"$@
		touch user.txt
	elif [ $1 == "upload_file" ] || [ $1 == "set_url" ] || [ $1 == "upload_folder" ] || [ $1 == "delete_file" ] || [ $1 == "delete_folder" ] || [ $1 == "sync" ] || [ $1 == "show_data" ] || [ $1 == "config" ]; then
		tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
		if [ $tym -gt 900 ]; then
			rm user.txt
			touch user.txt
			echo "session timed out, please login"
		else	  
			python3 linuxclient.py "--"$@
			touch user.txt
		fi	
	elif [ $1 == "observe" ] || [ $1 == "version" ] || [ $1 == "server" ] || [ $1 == "info" ] || [ $1 == "status" ]; then
		tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
		if [ $tym -gt 900 ]; then
			rm user.txt
			touch user.txt
			echo "session timed out, please login"
		else	  
			python3 linuxclient.py "--"$@
			touch user.txt
		fi		
	elif [ $1 == "download_file" ] || [ $1 == "download_folder" ]; then
		tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
		if [ $tym -gt 900 ]; then
			rm user.txt
			touch user.txt
			echo "session timed out, please login"
		else	  
			python3 linuxclient.py "--"$@
			touch user.txt
		fi	
	else
		echo "invalid argument, use 'spc info' command for help"
	fi
elif [ $# -eq 2 ]; then
	if [ $1 == "en-de" ]; then
		if [ $2 == "list" ] || [ $2 == "update" ]; then 
			tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
			if [ $tym -gt 900 ]; then
				rm user.txt
				touch user.txt
				echo "session timed out, please login"
			else	  
				python3 linuxclient.py "--"$2
				touch user.txt
			fi	
		else
			echo "invalid arguments, use 'spc info' command for help"	
		fi
	else
		echo "invalid arguments, use 'spc info' command for help"
	fi
elif [ $# -eq 3 ]; then
	if [ $1 == "en-de" ] && [ $2 == "update" ]; then
		tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
		if [ $tym -gt 900 ]; then
			rm user.txt
			touch user.txt
			echo "session timed out, please login"
		else	  
			python3 linuxclient.py "--update1" $3
			touch user.txt
		fi	
	elif [ $1 == "en-de" ] && [ $2 == "dump" ]; then
		tym=$(( $(date +%s) - $(stat -c%X user.txt) ))
		if [ $tym -gt 900 ]; then
			rm user.txt
			touch user.txt
			echo "session timed out, please login"
		else	  
			python3 linuxclient.py "--dump" $3
			touch user.txt
		fi	
	else
		echo "invalid arguments, use 'spc info' command for help"
	fi							
else
	echo "invalid number of arguments, use 'spc info' command for help"
fi	