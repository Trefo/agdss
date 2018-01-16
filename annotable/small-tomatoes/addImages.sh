#!/usr/bin/env bash
#This script adds all files in its current directory to the images stored on the AgDSS server.
#It takes one argument, which is the category for all the files that will be added
#
SERVER="localhost:8000"
URL="/webclient/addImage"
echo "Category is $1"
if [ "$#" -lt 1 ]
then
    echo "Category is required"
    exit 1
fi
shopt -s nullglob
for file in *.JPG; do
    echo $file
	curl --data "path=$(pwd)&image_name=$file&category=$1" "$SERVER$URL"
done
