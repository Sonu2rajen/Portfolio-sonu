@echo off
:: ============================================================
::  TEST MODE - Only scrapes 5 ASINs to verify everything works
:: ============================================================
echo.
echo  ================================================
echo   SUPPRESSION MONITOR - TEST MODE (5 ASINs only)
echo  ================================================
echo.
echo  Running test with only 5 ASINs...
echo  This should complete in 2-3 minutes.
echo.

cd /d "D:\admin\Desktop\Suppresstion-click"
python main.py --test

echo.
echo  ================================================
echo   TEST COMPLETE!
echo   Check: output folder for the Excel file
echo   Check: logs folder for detailed log
echo   Check: sonurajendran2@gmail.com for test email
echo  ================================================
echo.
pause
