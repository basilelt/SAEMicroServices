@echo off
:: Requires administrative privileges

:: Define DNS records
setlocal EnableDelayedExpansion
set "DNS_RECORDS=127.0.0.1 pgadmin.sae.local^
127.0.0.1 api.sae.local^
127.0.0.1 sae.local"

:: Backup current hosts file
copy C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.backup

:: Append DNS records to hosts file
for %%i in (%DNS_RECORDS%) do (
    echo %%i >> C:\Windows\System32\drivers\etc\hosts
)

echo DNS records have been added to your hosts file.