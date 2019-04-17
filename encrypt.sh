#!/usr/bin/env bash

# Encrypts a file or directory

# encrypt usage: ./crypto.sh <file/directory to encrypt>

# zip up the directory, then encrypt, then delete zip and
# original directory

# WARNING: DO NOT INCLUDE THE ENDING "/" WHEN ENCRYPTING A FOLDER
zip -r -X "$1.zip" $1

echo "$1.zip"

openssl aes-256-cbc -a -salt -in "$1.zip" -out "$1.zip.enc"

rm -rf $1
rm "$1.zip"

