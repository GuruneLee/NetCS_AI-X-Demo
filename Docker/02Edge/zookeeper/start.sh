sudo docker stop edge-broker
sudo docker rm -f edge-broker
sudo docker stop edge-zookeeper
sudo docker rm -f edge-zookeeper

sudo docker run -d --net=host --name edge-zookeeper dlckdgk4858/aix-edge-zookeeper:dev
