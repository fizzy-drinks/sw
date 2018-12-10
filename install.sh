#!/bin/bash
SW_URL=https://raw.githubusercontent.com/gabrielchiconi/sw/master/sw.py
SW_PATH=$(realpath ~/.sw/bin)

mkdir -p $SW_PATH
curl -o $SW_PATH/sw $SW_URL
echo "
PATH=$PATH:$SW_PATH" >> ~/.bashrc
