#!/bin/bash
# remove early ran container
sudo docker stop edge-consumer-producer 
sudo docker rm -f edge-consumer-producer

# docker build & run /bin/bash
sudo docker build -t dlckdgk4858/aix-edge-consumer-producer:dev .
sudo docker run -d --net=host --runtime=nvidia --name edge-consumer-producer dlckdgk4858/aix-edge-consumer-producer:dev

# get logs from container
watch sudo docker logs edge-consumer-producer


