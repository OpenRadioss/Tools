#!/bin/bash

cd inp2rad
pip3 install .
cd ..
cd build
pyinstaller --onefile ../inp2rad/inp2rad.py
python3 install.py
cd ..
