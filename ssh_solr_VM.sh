#!/usr/bin/env bash

# Lets you ssh in to the VM as sudo Ubuntu user. Need valid RSA key to
# access the VM

# Usage: ./ssh_solr_VM.sh <Access key.pem>

ssh -i $1 ubuntu@ec2-52-14-160-147.us-east-2.compute.amazonaws.com
