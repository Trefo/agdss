#!/usr/bin/env bash
#This script adds all files in its current directory to the images stored on the AgDSS server.
#It takes one argument, which is the category for all the files that will be added
#
#SERVER="162.243.97.220"
SERVER="localhost:80"
URL="/webclient/addImage"
echo "Categories are $1"
if [ "$#" -lt 1 ]
then
    echo "Categories are required"
    exit 1
fi
IMAGE_TYPES="{jpg, jpeg, png, bmp}"
shopt -s nullglob nocaseglob
for file in *.jpg *.jpeg *.png *.bmp; do
    curl --data "path=$(pwd)&image_name=$file&categories=$1" "$SERVER$URL"
done
