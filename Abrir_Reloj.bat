@echo off
title Iniciando Reloj Analogico Pro...
color 0A

echo.
echo ================================================
echo       RELOJ ANALOGICO PRO - OSKAR EDITION
echo ================================================
echo.
echo Iniciando aplicacion...
echo.

REM Ejecutar el reloj con Python
python main.py

REM Si hay error, pausar para ver el mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo iniciar el reloj.
    echo.
    pause
)