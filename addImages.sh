#!/usr/bin/env bash
SERVER="localhost:8000"
URL="/webclient/addImage"
CATEGORY=apple
IMAGE_TYPES="{jpg, jpeg, png, bmp}"
shopt -s nullglob
for file in *.jpg *.jpeg *.png *.bmp; do
    curl --data "path=$(pwd)&image_name=$file&category=$CATEGORY" "$SERVER$URL"
done