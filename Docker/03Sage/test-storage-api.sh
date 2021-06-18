#!/bin/bash

# stop early container
sudo docker build -t dlckdgk4858/aix-storage-api:dev .
sudo docker push dlckdgk4858/aix-storage-api:dev

# deploy pod
kubectl delete -f ../../kubernetes/storage-api.yaml
kubectl create -f ../../kubernetes/storage-api.yaml

# get NodePort
kubectl get svc

# open shell of the pod
# bkubectl exec -it $(kubectl get pod -l app=aix-storage-api -o jsonpath="{.items[0].metadata.name}") -- /bin/bash

# logs the pod
watch kubectl logs $(kubectl get pod -l app=aix-storage-api -o jsonpath="{.items[0].metadata.name}")
