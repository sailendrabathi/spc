#bin/bash
if [ -e  /usr/bin/spc ]; then
	echo "spc already exists in" /usr/bin/ 
	echo "Removing the existing spc file ..."
	sudo rm /usr/bin/spc
fi
echo "Creating spc in" /usr/bin
sudo ln -s $(pwd)/spc /usr/bin/
echo "spc install completed."