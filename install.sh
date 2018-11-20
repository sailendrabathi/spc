#bin/bash
if [ -e  $HOME/.local/bin/spc ]; then
	echo "spc already exists in" $HOME/.local/bin/ 
	echo "Removing the existing spc file ..."
	rm $HOME/.local/bin/spc
fi
echo "Creating spc in" $HOME/.local/bin
ln -s $(pwd)/spc $HOME/.local/bin/
echo "spc install completed."