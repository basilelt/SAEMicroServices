@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

setlocal

:: Hardcoded IP address and hostname
set "ip1=172.0.0.1"
set "hostname1=sae.local"

set "ip2=172.0.0.1"
set "hostname2=pgadmin.sae.local"

set "ip3=172.0.0.1"
set "hostname3=api.sae.local"

:: The location of the hosts file
set "hosts=%windir%\System32\drivers\etc\hosts"

:: Create a temporary file
set "tempfile=%temp%\temp.txt"

:: Add the new entries to the temporary file
echo %ip1% %hostname1% > "%tempfile%"
echo %ip2% %hostname2% > "%tempfile%"
echo %ip3% %hostname3% > "%tempfile%"

:: Append the current hosts file to the temporary file
type "%hosts%" >> "%tempfile%"

:: Replace the hosts file with the temporary file
copy /y "%tempfile%" "%hosts%"

:: Clean up
del "%tempfile%"
endlocal