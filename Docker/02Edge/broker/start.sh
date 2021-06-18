sudo docker stop edge-broker
sudo docker rm -f edge-broker
sudo docker run -d --net=host --name edge-broker dlckdgk4858/aix-edge-broker:dev
