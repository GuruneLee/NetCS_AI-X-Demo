import time
import sys
import cv2

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='172.30.84.94:9092')
topic = 'video3'
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def emit_video():
    print('start emitting')

    video = cv2.VideoCapture(0)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # png might be too large to emit

        result, data = cv2.imencode('.jpg', frame, encode_param)

        future = producer.send(topic, data.tobytes())

        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break

        #print('.', end='', flush=True)

        # to reduce CPU usage
        time.sleep(0.2)
    print()

    #video.release()

    print('done')


if __name__ == '__main__':
    emit_video()
