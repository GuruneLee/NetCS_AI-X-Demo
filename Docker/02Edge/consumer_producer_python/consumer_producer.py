from flask import Flask, Response
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import cv2
import numpy as np
import datetime

import glob
import os
import time

NULL_IMG = np.zeros((100,100,3), dtype=np.uint8)
NULL_IMG_BIN = cv2.imencode('.jpeg', NULL_IMG)[1].tobytes()

consumer2 = KafkaConsumer('video3', bootstrap_servers='172.30.84.94:9092')
producer = KafkaProducer(bootstrap_servers='172.30.84.61:9092')
topic = 'my-topic'
path3 = "/home/netcs/frames/source3/"

app = Flask(__name__)


def kafkastream():
    print("bcdf")

    count = 0
    video_num = 0
    now = datetime.datetime.now()
    
    # yolo-detection start
    ## preparing the dataset, weight, labels, config
    labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                        dtype="uint8")
    weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
    configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

    ## preparing the dnn using config/weight
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


    ## I DON'T KNOW WHAT IT IS
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


    # toProduce: 이미지 바이너리를 담을 리스트
    # isPushed: 담기 시작했는지 알리는 flag
    # last: 마지막으로 담긴 객체의 index
    # len: toProduce의 사이즈
    toProduce = []
    isPushed = False
    last = -1
    length = 0

    ## get messages from 'my-topic' topic
    ## in each loop, whole process is for just one video frame
    for message in consumer2:
        
        # 한 장의 프레임에서 yolo를 이용해 object detection하는 부분
        array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
        image = cv2.imdecode(array,1)
        (H, W) = image.shape[:2] # image -> img
        
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

        # object가 디텍팅 되면, 그 위에 박싱을 하는 부분
        ## isDetected: 원하는 객체가 탐지됐는가를 담는 flag 
        isDetected = False
        if len(idxs) > 0:
            # 프레임에서 발견된 tag의 종류 저장
            tags = set()

            for i in idxs.flatten():
                tags.add(LABELS[classIDs[i]])
                person_flag = 0
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # 원하는 객체가 발견되면, push상태로 만듦
            isDetected = "chair" in tags
            if isDetected and not isPushed:
                isPushed = True

        # push가 시작되면 모든 프레임을 append함  
        # last와 length를 업데이트  
        if isPushed:
            toProduce.append(cv2.imencode('.jpeg', image)[1].tobytes())
            length = len(toProduce)
            if isDetected:
                last = length-1
            # push가 끝날 조건
            # 1) 6번의 x / 2) 길이가 200 이상
            if last+6 <= length or length >= 200:
                for bimg in toProduce:
                    err = producer.send(topic, bimg)
                    producer.flush()
                    try:
                        err.get(timeout=10)
                    except KafkaError as e:
                        print(e)
                        break
                # 저장 할 비디오를 다 보냈으면 빈 이미지를 보내서 flag를 세움
                err = producer.send(topic, NULL_IMG_BIN)
                producer.flush()
                try:
                    err.get(timeout=10)
                except KafkaError as e:
                    print(e)
                    break
                # 다시 push할 상태가 아니게 만들기
                isPushed = False
                toProduce.clear()
        # push할 상태가 아닐 땐 항상 빈 이미지를 보냄
        else:
            err = producer.send(topic, NULL_IMG_BIN)
            producer.flush()
            try:
                err.get(timeout=10)
            except KafkaError as e:
                print(e)
                break

            # ### I GEUSS THAT THIS LINE IS FIT TO PRODUCE THE DETECTED IMAGE
            # if "chair" in tags:
            #     ## producing
            #     future = producer.send(topic, cv2.imencode('.jpeg', image)[1].tobytes())
            #     producer.flush()
        
            #     try:
            #         future.get(timeout=10)
            #     except KafkaError as e:
            #         print(e)
            #         break


        ## encode the image to binary
        data = cv2.imencode('.jpeg', image)[1].tobytes()        
        
        ## yield the image-binary for Flask streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')


@app.route('/video3')
def video3():
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("bcdf")
    #kafkastream()
    app.run(host='0.0.0.0',debug=True, threaded=True)
    print("bcdf")

