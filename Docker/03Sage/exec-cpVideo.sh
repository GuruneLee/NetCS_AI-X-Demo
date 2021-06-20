sudo rm result_video/*.*
kubectl cp $(kubectl get pod -l app=aix-storage-api -o jsonpath="{.items[0].metadata.name}"):mnt/video result_video
