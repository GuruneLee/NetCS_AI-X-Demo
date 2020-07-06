from flask import Flask, Response
from kafka import KafkaConsumer
import cv2
import numpy as np
import datetime

import glob
import os
import time

consumer2 = KafkaConsumer('my-topic', bootstrap_servers='172.30.84.92:9092', api_version=(0, 10, 1))
path3 = "/home/netcs/frames/source3/"

def kafkastream():
        print("bcdf")
        count = 0
        video_num = 0
        now = datetime.datetime.now()
        for message in consumer2:
                #print("yogi")
                array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
                image = cv2.imdecode(array,1)
                cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Image', image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                #count += 1;
                #count_str = str(count)
                #cv2.imwrite("/home/tein/kafka-python-video-streaming/src/result_img/test_" + count_str  +".jpg", image)
if __name__ == '__main__':
        print("bcdf")
        kafkastream()
        print("egd")

