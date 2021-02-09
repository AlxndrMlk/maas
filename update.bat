@echo off
echo Welcome to MAAS - Update
echo Loading...
echo.
call activate.bat MAAS
python.exe scripts/tools/update.py
echo Done
echo Thank you!
echo.
