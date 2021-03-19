#!/bin/sh

curl --silent "https://api.digitalocean.com/v2/images?per_page=999&type=distribution" -H "Authorization: Bearer $DO_API_TOKEN"
