#!/bin/sh

curl --silent "https://api.digitalocean.com/v2/account/keys" -H "Authorization: Bearer $DO_API_TOKEN"
