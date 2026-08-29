@echo off
:: ============================================================
::  RUN SUPPRESSION MONITOR NOW (Manual trigger)
:: ============================================================
echo.
echo  ================================================
echo   SUPPRESSION MONITOR - MANUAL RUN
echo   Clicktech ^| Amazon.in
echo  ================================================
echo.
echo  Starting suppression check...
echo  (This will take 30-60 mins for 599 ASINs)
echo.

cd /d "D:\admin\Desktop\Suppresstion-click"
python main.py

echo.
echo  ================================================
echo   RUN COMPLETE. Check output folder for results.
echo  ================================================
echo.
pause
