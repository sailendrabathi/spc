#bin/bash
if [ -e  $HOME/.local/bin/spc ]; then
	echo "spc is already exists in" $HOME/.local/bin/ 
	echo "Removing the existing spc file ..."
	rm $HOME/.local/bin/spc
fi
ln -s $(pwd)/spc $HOME/.local/bin/