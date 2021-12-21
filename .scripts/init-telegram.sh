#!/bin/bash

# create .config files (key, telegram_token1)
# input apikey
# encrypt json in env
# cp files from templates

WORKDIR=test #app

if [ ! -f $WORKDIR ]; then
mkdir $WORKDIR
fi
cd $WORKDIR 
mkdir .config 

DIR=.config

DEST=$DIR/key
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode(), end='')" > $DEST
echo "Saved encryption key to $DEST..."

DEST=$DIR/telegram.json
echo -n "Enter Telegram Token: "
read -s KEY_TELEGRAM
echo -n -e "{\n\t\"api_key\": \"${KEY_TELEGRAM}\"\n}" > $DEST
echo -e "\nSaved telegram key to $DEST..."

### 
ls $DIR | grep "\.json" | while read file 
do
echo $file 
done

### Export variables in future sessions
# echo "
# set -a
# source $PWD/.env
# set +a" >> $PWD/.venv/bin/activate

SRC=/home/lyx
DIR=Py/Telegram