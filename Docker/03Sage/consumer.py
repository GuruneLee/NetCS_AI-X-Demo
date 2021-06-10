from flask import Flask, Response
from kafka import KafkaConsumer
import cv2
import numpy as np
import datetime

import glob
import os
import time

consumer2 = KafkaConsumer('my-topic', bootstrap_servers='172.30.84.61:9092', api_version=(0, 10, 1))
result_path = "/result/video/"

app = Flask(__name__)

def kafkastream():
    print("bcdf")
    count = 0
    video_num = 0
    now = datetime.datetime.now()

    vlen = 0
    
    video_num = -1
    frame_array = []
    for message in consumer2:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')
        #print("yogi")
        array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
        image = cv2.imdecode(array,1)
        
        frame_array.append(image)
        vlen += 1

        if vlen == 100:
            vlen = 0
            video_num += 1
            video_path = result_path + "video_" + str(video_num)+".mp4"
            h = image.shape[0]
            w = image.shape[1]
            fps = 10
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            out = cv2.VideoWriter(video_path, fourcc, fps, (w,h))

            if not out.isOpened():
                print('File open failed!')
            else:
                for i in range(len(frame_array)):
                    out.write(frame_array[i])
                out.release()
                frame_array = []
                print(video_path + ' is generated\n')
        #if cv2.waitKey(25) & 0xFF == ord('q'):
        #    break
                #count += 1;
                #count_str = str(count)
                #cv2.imwrite("/home/tein/kafka-python-video-streaming/src/result_img/test_" + count_str  +".jpg", image)

@app.route('/video')
def video():
    return Response(kafkastream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("bcdf")
    #kafkastream()
    app.run(host='0.0.0.0', debug=True, threaded=True)
    print("egd")

