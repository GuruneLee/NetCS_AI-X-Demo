sudo docker stop end-producer
sudo docker rm -f end-producer
sudo docker run -d --net=host --privileged --device=/dev/video0:/dev/video0 -it --name end-producer dlckdgk4858/aix-end-producer:dev
