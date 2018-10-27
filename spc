#!/bin/bash

if [ $# -eq 1 ] 
then
	if [ $1 == "signup" ] || [ $1 == "login" ] || [ $1 == "upload_file" ] || [ $1 == "set_url" ] || [ $1 == "logout" ] || [ $1 == "upload_folder" ] || [ $1 == "delete_file" ] || [ $1 == "delete_folder" ] || [ $1 == "sync" ] || [ $1 == "show_data" ] 
	then 
		python3 linuxclient.py "--"$@
	else
		echo "invalid argument"
	fi		
else
	echo "invalid number of arguments"
fi	