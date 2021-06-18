
from flask import Flask, Response
from kafka import KafkaConsumer
import cv2
import numpy as np
import datetime

import glob
import os
import time

NULL_IMG = np.zeros((100,100,3), dtype=np.uint8)
NULL_IMG_BIN = cv2.imencode('.jpeg', NULL_IMG)[1].tobytes()

consumer2 = KafkaConsumer('my-topic', bootstrap_servers='172.30.84.61:9092', api_version=(0, 10, 1))
result_path = "/mnt/video/"

app = Flask(__name__)


isStored = False
isNewVideo = False

# video
h = 381
w = 508
fps = 10
fourcc = cv2.VideoWriter_fourcc(*'DIVX')



def kafkastream():
    global isStored
    global isNewVideo
    frame_array = []
    for message in consumer2:
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')
        print(message.value)
        # check if new video is started
        # check if frames to be stored
        if message.value == NULL_IMG_BIN:
            isStored = True
        else:
            isStored = False
            if not isNewVideo:
                isNewVideo = True

        # print(str(isNewVideo) + ', ' + str(isStored))

        
        if isNewVideo and not isStored:
            array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
            image = cv2.imdecode(array,1)
            frame_array.append(image)

      
        if isNewVideo and isStored:
            print("start to store a video")
            video_path = time.strftime("%Y%m%d-%H%M%S") + ".mp4"
            out = cv2.VideoWriter(video_path, fourcc, fps, (w,h))
            if not out.isOpened():
                print('File open failed!')
            else:
                for i in range(len(frame_array)):
                    out.write(frame_array[i])
                out.release()
                frame_array.clear()
                print(video_path + ' is generated\n')
            isNewVideo = False
        




        # #print("yogi")
        # array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
        # image = cv2.imdecode(array,1)
        
        # frame_array.append(image)
        # vlen += 1

        # if vlen == 100:
        #     vlen = 0
        #     video_num += 1
        #     video_path = result_path + "video_" + str(video_num)+".mp4"
        #     h = image.shape[0]
        #     w = image.shape[1]
        #     fps = 10
        #     fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        #     out = cv2.VideoWriter(video_path, fourcc, fps, (w,h))

        #     if not out.isOpened():
        #         print('File open failed!')
        #     else:
        #         for i in range(len(frame_array)):
        #             out.write(frame_array[i])
        #         out.release()
        #         frame_array = []
        #         print(video_path + ' is generated\n')

@app.route('/video')
def video():
    return Response(kafkastream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("bcdf")
    #kafkastream()
    app.run(host='0.0.0.0', debug=True, threaded=True)
    print("egd")

