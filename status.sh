#!/bin/sh

ansible locust -m command -a "systemctl status locust" -i digital_ocean.py -u root
