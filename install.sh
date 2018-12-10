#!/bin/bash
SW_URL=https://raw.githubusercontent.com/gabrielchiconi/sw/master/sw.py
SW_PATH=$(realpath ~/.sw/bin)

mkdir -p $SW_PATH
echo "Downloading sw..."
curl -o $SW_PATH/sw $SW_URL
echo "Done. Adding to rc..."
echo "
PATH=\"$SW_PATH:\$PATH\"" >> ~/.bashrc
echo "Done"
echo "Restart your shell to use sw!"

