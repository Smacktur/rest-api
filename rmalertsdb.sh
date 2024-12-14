#!/bin/sh
echo "Removing old alerts.db file (if exists)..."
rm -f /data/alerts.db
exec "$@"