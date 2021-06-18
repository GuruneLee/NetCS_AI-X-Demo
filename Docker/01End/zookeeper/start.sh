sudo docker stop end-broker
sudo docker rm -f end-broker

sudo docker stop end-zookeeper
sudo docker rm -f end-zookeeper

sudo docker run -d --net=host --name end-zookeeper dlckdgk4858/aix-end-zookeeper:dev
