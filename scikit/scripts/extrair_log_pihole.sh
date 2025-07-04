#!/bin/bash
docker exec pi-hole_server_1 cat /var/log/pihole.log > /home/umbrel/sirius/scikit/data/pihole_temp.log
