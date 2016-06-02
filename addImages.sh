#!/usr/bin/env bash
SERVER="localhost:8000"
URL="/webclient/addImage"
echo "Category is $1"
if [ "$#" -lt 1 ]
then
    echo "Category is required"
    exit 1
fi
IMAGE_TYPES="{jpg, jpeg, png, bmp}"
shopt -s nullglob
for file in *.jpg *.jpeg *.png *.bmp; do
    curl --data "path=$(pwd)&image_name=$file&category=$1" "$SERVER$URL"
done