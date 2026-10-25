@echo off
py -3 "%~dp0organiseur_fichiers.py"
if errorlevel 1 python "%~dp0organiseur_fichiers.py"
pause
