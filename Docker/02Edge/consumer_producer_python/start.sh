sudo docker stop edge-consumer-producer 
sudo docker rm -f edge-consumer-producer
sudo docker run -d --net=host --runtime=nvidia --name edge-consumer-producer dlckdgk4858/aix-edge-consumer-producer:dev
