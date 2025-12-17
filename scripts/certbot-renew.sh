#!/bin/sh
# Certbot auto-renewal script
# This script runs in a loop, renewing certificates every 12 hours

trap exit TERM

while :; do
    certbot renew
    sleep 12h & wait ${!}
done
