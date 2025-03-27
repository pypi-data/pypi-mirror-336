@echo off
rem This is to set up the essential pre-requisites for for paxo: uv
rem
rem This file should be accessible in g: drive, so that it can be run from the command prompt.
rem Put it in G:\Shared drives\devx\paxo

rem Set the console title
title paxo initial setup
echo Welcome to paxo initial setup

setlocal
set batfile=%~dp0

rem check if uv is installed
uv version
if %errorlevel% equ 0 (
    echo uv is already installed, update it
    call uv self update
    goto :uv-installed
)

rem install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

rem add uv to the path, if necessary
uv version
if %errorlevel% neq 0 (
    set PATH=%USERPROFILE%\.local\bin;%PATH%
)

:uv-installed

echo install paxo
rem force install, which will get the latest version even if already installed
call uv tool install --force mainframe-paxo
if %errorlevel% neq 0 (
    echo paxo installation failed
    goto :finish
)

goto :finish

:finish
if %errorlevel% neq 0 (
    echo paxo initial install failed
    pause
    exit /b %errorlevel%
)
echo paxo initial install succeeded
echo if you want to use paxo, you need to open a new console window
echo and run the 'paxo' command.
echo 'paxo initial-setup' will continue the setup of your machine.
pause
exit /b 0
