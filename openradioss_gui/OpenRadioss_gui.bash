#!/usr/bin/bash

# Copyright 1986-2026 Altair Engineering Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Path to the Python script
script_path="OpenRadioss_gui.py"
if [ ! -d  $HOME/.OpenRadioss_GUI ]
then 
     mkdir $HOME/.OpenRadioss_GUI
fi
if [ ! -d  $HOME/.OpenRadioss_GUI/__pycache__ ]
then
     mkdir $HOME/.OpenRadioss_GUI/__pycache__
fi

# Call the Python script using Python 3
echo $HOME/.OpenRadioss_GUI/__pycache__
export PYTHONPYCACHEPREFIX=$HOME/.OpenRadioss_GUI/__pycache__

python3 "$script_path"
