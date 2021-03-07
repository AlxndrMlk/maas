@echo off
echo Welcome to MAAS - Update
echo Loading...
echo.
call activate.bat MAAS
python.exe scripts/tools/update.py
conda env update --file environment.yml
echo Done
echo Thank you!
echo.
