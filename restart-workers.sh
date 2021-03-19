#!/bin/sh

ansible locust -m systemd -a "service=locust state=restarted" -i digital_ocean.py -u root
