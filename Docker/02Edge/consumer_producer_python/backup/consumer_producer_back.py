from flask import Flask, Response
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import cv2
import numpy as np
import datetime

import glob
import os
import time

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
    #for message in consumer2:
        #yield (b'--frame\r\n'               b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')
    #array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
    #image = cv2.imdecode(array,1)

        ## yolo-detection start
    labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                        dtype="uint8")
    weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
    configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])


    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


        #same as non gpu
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


    for message in consumer2:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')
        array = np.frombuffer( message.value, dtype = np.dtype('uint8'))
        image = cv2.imdecode(array,1)
        (H, W) = image.shape[:2] # image -> img
        #should be in loop
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

        #detected image proccessing
        if len(idxs) > 0:
            for i in idxs.flatten():
                person_flag = 0
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        #producing
        data = cv2.imencode('.jpeg', image)[1].tobytes()
        future = producer.send(topic, data)
        producer.flush()
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break
        #time.sleep(0.2)
        ## let send an image to new_topic as new_producer
        #cv2.imshow('Image', image)
        #if cv2.waitKey(25) & 0xFF == ord('q'):
        #      break

@app.route('/video3')
def video3():
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("bcdf")
    #kafkastream()
    app.run(host='0.0.0.0',debug=True, threaded=True)
    print("bcdf")

