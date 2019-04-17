#!/usr/bin/env bash

# usage: ./decrypt.sh <.enc file to decrypt>

openssl aes-256-cbc -d -a -salt -in $1 -out sensitive.zip
unzip sensitive.zip
rm sensitive.zip
