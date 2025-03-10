#!/bin/bash

GREEN="\e[32m"
BG_BLUE="\e[44m"
BOLD="\e[1m"
RESET="\e[0m"

sudo apt install -y build-essential git
sudo apt install -y cmake
sudo apt install -y libasound2-dev libx11-dev libxrandr-dev libxi-dev libgl1-mesa-dev libglu1-mesa-dev libxcursor-dev libxinerama-dev libwayland-dev libxkbcommon-dev

git clone https://github.com/raysan5/raylib.git raylib
cd raylib
mkdir build && cd build
cmake -DBUILD_SHARED_LIBS=ON ..
make
sudo make install

sudo ldconfig
cd ../..
rm -rf raylib/

echo -e "${BOLD}${GREEN}${BG_BLUE}"
echo "----------------------------------------"
echo "  Program Finished! Raylib is installed  "
echo "----------------------------------------"
echo -e "${RESET}"
