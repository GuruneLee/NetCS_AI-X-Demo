#!/bin/bash

# git pull
git pull origin master

# remove early ran container
sudo docker stop edge-consumer-producer 
sudo docker rm -f edge-consumer-producer

# docker build & run /bin/bash
sudo docker rmi -f dlckdgk4858/aix-edge-consumer-producer:dev
sudo docker build -t dlckdgk4858/aix-edge-consumer-producer:dev .
sudo docker run -d --net=host --runtime=nvidia --name edge-consumer-producer dlckdgk4858/aix-edge-consumer-producer:dev
# sudo docker run -it --net=host --runtime=nvidia --name edge-consumer-producer dlckdgk4858/aix-edge-consumer-producer:dev /bin/bash

# get logs from container
watch sudo docker logs edge-consumer-producer


