@echo off
echo ...
echo Welcome to MAAS - Data Refresher
echo Loading...
echo.
call activate.bat MAAS
@REM python.exe scripts/tools/refresh_data.py
python.exe scripts/tools/update_pdf_data.py
echo Done
echo Thank you!
echo.
