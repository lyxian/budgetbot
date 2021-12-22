#!/bin/bash

if [ -f secrets ]; then

if [ ! -f .config ]; then
mkdir .config
fi

DIR=.config
DEST=$DIR/key
key=`python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode(), end='')"`
echo -n $key > $DEST
echo -e "Saved encryption key to $DEST...\n"

while read line
do 
name=`echo $line | cut -d "=" -f1`
value=`echo $line | cut -d "=" -f2-`
secret=`python3 -c "from cryptography.fernet import Fernet; print(Fernet('${key}'.encode()).encrypt('${value}'.encode()).decode(), end='')"`
DEST=$DIR/secret_$name
echo -n "$secret" > $DEST
echo "Saved $name key to $DEST..."
done < secrets

rm secrets
else 
echo "No secrets found, exiting..."
fi