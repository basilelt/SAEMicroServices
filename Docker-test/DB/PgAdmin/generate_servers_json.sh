#!/bin/bash

# generate_servers_json.sh
cat <<EOF
{
    "Servers": {
        "1": {
            "Name": "${POSTGRES_DB}",
            "Group": "Servers",
            "Host": "db",
            "Port": 5432,
            "Username": "${POSTGRES_USER}",
            "Password": "${POSTGRES_PASSWORD}",
            "MaintenanceDB": "postgres",
            "SSLMode": "prefer",
            "ConnectTimeout": 10
        }
    }
}
EOF