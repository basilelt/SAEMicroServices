#!/bin/bash

# Define DNS records
DNS_RECORDS="127.0.0.1 pgadmin.sae.local
127.0.0.1 api.sae.local
127.0.0.1 sae.local"

# Backup current hosts file
sudo cp /etc/hosts /etc/hosts.backup

# Add DNS records to hosts file
echo "$DNS_RECORDS" | sudo tee -a /etc/hosts > /dev/null

echo "DNS records added to /etc/hosts."