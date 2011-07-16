@echo off
del %1.exe
rem set base=%Python_home%\Tools\pyinstaller-1.3
set base=%Python_home%\Tools\pyinstaller
%base%\Makespec.py --onefile --upx %1.py
%base%\Build.py %1.spec

rem for trunk version
move .\dist\%1.exe .

del /Q %1.spec
del /Q warn%1.txt
rem del /Q *.pyc

rem clean For version 1.3
rem rd /Q /S build%1

rem clean for trunk version
rd /Q /S build
rd /Q /S dist
del /Q logdict*.log
