#!/bin/bash

rm -rf ~/.local/share/Trash/*

if [ "$(ls -A /home/vinicius/Downloads)" ]; then
    for file in /home/vinicius/Downloads/*; do
        gio trash "$file"
    done
fi