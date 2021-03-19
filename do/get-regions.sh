#!/bin/sh

curl --silent "https://api.digitalocean.com/v2/regions" -H "Authorization: Bearer $DO_API_TOKEN"
