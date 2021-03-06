
from flask import Flask, Response
from kafka import KafkaConsumer
import cv2
import numpy as np
import datetime

import glob
import os
import time

NULL_IMG = np.zeros((100,100,3), dtype=np.uint8)
NULL_IMG_BIN = '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x02\x01\x01\x01\x01\x01\x02\x01\x01\x01\x02\x02\x02\x02\x02\x04\x03\x02\x02\x02\x02\x05\x04\x04\x03\x04\x06\x05\x06\x06\x06\x05\x06\x06\x06\x07\t\x08\x06\x07\t\x07\x06\x06\x08\x0b\x08\t\n\n\n\n\n\x06\x08\x0b\x0c\x0b\n\x0c\t\n\n\n\xff\xdb\x00C\x01\x02\x02\x02\x02\x02\x02\x05\x03\x03\x05\n\x07\x06\x07\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\xff\xc0\x00\x11\x08\x00d\x00d\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfe\x7f\xe8\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00(\xa2\x8a\x00\xff\xd9'

consumer2 = KafkaConsumer('my-topic', bootstrap_servers='172.30.84.61:9092', api_version=(0, 10, 1))
result_path = "/mnt/video/"

app = Flask(__name__)


isStored = False
isNewVideo = False

# video
# h = 381
# w = 508
# fps = 10
# fourcc = cv2.VideoWriter_fourcc(*'XVID')



def kafkastream():
    global isStored
    global isNewVideo
    frame_array = []

    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    for message in consumer2:
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')
    
        # check if new video is started
        # check if frames to be stored
        if message.value == NULL_IMG_BIN:
            print("image is empty")
            isStored = True
        else:
            isStored = False
            if not isNewVideo:
                isNewVideo = True

        # print(str(isNewVideo) + ', ' + str(isStored))

        
        if isNewVideo and not isStored:
            if message.value != NULL_IMG_BIN:
                array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
                image = cv2.imdecode(array,1)
                frame_array.append(image)
                cv2.imshow('Image', image)

      
        if isNewVideo and isStored:
            print("start to store a video")
            h = 381
            w = 508
            fps = 10
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            video_path = result_path + time.strftime("%Y%m%d-%H%M%S") + ".mp4"
            out = cv2.VideoWriter(video_path, fourcc, fps, (w,h))
            if not out.isOpened():
                print('File open failed!')
            else:
                for i in range(len(frame_array)):
                    out.write(frame_array[i])
                out.release()
                frame_array = []
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

