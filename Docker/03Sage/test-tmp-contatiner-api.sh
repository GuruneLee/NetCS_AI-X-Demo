##git config credential.helper 'cache --timeout=3600'
git pull origin master

# stop early container
sudo docker stop test-api
sudo docker rm test-api
sudo docker rmi dlckdgk4858/aix-storage-api:dev
sudo docker build -t dlckdgk4858/aix-storage-api:dev .
sudo docker push dlckdgk4858/aix-storage-api:dev

# run
sudo docker run -it --net=host --name test-api dlckdgk4858/aix-storage-api:dev /bin/bash
