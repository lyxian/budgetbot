#!/bin/bash

if [ -d .venv ]; then 
echo "venv dir found...installing packages..."

deactivate
. .venv/bin/activate

lines=`cat README.md | grep -n "##Packages" | cut -d : -f1 | tr '\n' ',' | rev | cut -c 2- | rev`

sed -n ${lines}p README.md | head -n -1 | tail -n +2 | while read module
do
echo Installing $module...
# pip install $module
done
else
echo "venv dir NOT found...exiting..."
fi