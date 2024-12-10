@echo OFF

cd inp2rad
pip install .
cd ..
cd build
pyinstaller --onefile ..\inp2rad\inp2rad.py
python install.py
cd ..

