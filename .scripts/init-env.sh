#!/bin/bash

appPath=$PWD/app
secretDir=$PWD/.config

echo "DEBUG_MODE=True (y/n)"
read answer
if [ `echo $answer | grep "y\|Y"` ]; then
answer="True"
else
answer="False"
fi

echo -en "Enter PUBLIC_URL="
read url

# Create .env
echo "DEBUG_MODE=$answer
PUBLIC_URL=$url/" > $appPath/.env

# Append secrets
ls $secretDir | grep "^key\|^secret" | while read file
do
var=`echo $file | tr a-z A-Z`
echo $var=`cat $secretDir/$file` >> $appPath/.env
done
echo "ENV created in $appPath/.env"

# Update "activate"
if [[ `cat .venv/bin/activate | grep "set +a"` ]]; then 
echo "VENV already updated"
else
echo "
set -a
source $appPath/.env
set +a" >> $PWD/.venv/bin/activate
echo "VENV updated"
fi