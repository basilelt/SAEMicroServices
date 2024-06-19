@echo off
setlocal

:: Define DNS records
set DNS_RECORDS=127.0.0.1 pgadmin.sae.local^
127.0.0.1 api.sae.local^
127.0.0.1 sae.local

:: Backup current hosts file
copy C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.backup

:: Add DNS records to hosts file
echo %DNS_RECORDS% >> C:\Windows\System32\drivers\etc\hosts

echo DNS records added to hosts.