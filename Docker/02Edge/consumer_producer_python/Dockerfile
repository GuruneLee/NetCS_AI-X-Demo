FROM datamachines/cudnn_tensorflow_opencv:10.2_1.15.2_4.2.0-20200327

#Update & Install wget
RUN apt-get update
RUN apt-get install -y wget vim iputils-ping net-tools iproute2 dnsutils
RUN apt-get install -y python python-pip
RUN pip install numpy
RUN pip install flask
RUN pip install kafka

ADD consumer_producer.py /
RUN mkdir yolo-coco
WORKDIR /yolo-coco
ADD yolo-coco /yolo-coco
WORKDIR /

CMD python3 consumer_producer.py
