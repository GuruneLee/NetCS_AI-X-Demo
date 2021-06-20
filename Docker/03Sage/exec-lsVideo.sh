kubectl exec $(kubectl get pod -l app=aix-storage-api -o jsonpath="{.items[0].metadata.name}") -- ls /mnt/video
