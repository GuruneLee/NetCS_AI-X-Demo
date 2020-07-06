FROM ubuntu:18.04
MAINTAINER Geumseong Yoon <gsyoon@smartx.kr>

#Update & Install wget
RUN apt-get update
RUN apt-get install -y wget vim iputils-ping net-tools iproute2 dnsutils
RUN apt-get install -y python python-pip
RUN pip install numpy
RUN pip install flask
RUN pip install kafka

#Install required packages
RUN apt-get install -y build-essential cmake
RUN apt-get install -y pkg-config
RUN apt-get install -y libjpeg-dev libtiff5-dev libpng-dev
RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev
RUN apt-get install -y libv4l-dev v4l-utils
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN apt-get install -y libgtk2.0-dev

RUN apt-get install -y mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev
RUN apt-get install -y libatlas-base-dev gfortran libeigen3-dev
RUN apt-get install -y unzip

#Configure opencv
RUN mkdir opencv
WORKDIR /opencv
RUN wget https://github.com/opencv/opencv/archive/4.2.0.zip
RUN mv 4.2.0.zip opencv.zip
RUN wget https://github.com/opencv/opencv_contrib/archive/4.2.0.zip
RUN mv 4.2.0.zip opencv_contrib.zip
RUN unzip opencv.zip
RUN unzip opencv_contrib.zip
WORKDIR /opencv/opencv-4.2.0
RUN mkdir build
WORKDIR /opencv/opencv-4.2.0/build
ADD build.sh /opencv/opencv-4.2.0/build
RUN sh build.sh
#RUN CPUNUM=$(cat /proc/cpuinfo | grep processor | wc -l)
#RUN DIVCPU=$(expr $CPUNUM '/' 2)
#RUN make -j$DIVCPU
RUN make -j3
RUN make install
RUN ldconfig
WORKDIR /
ADD consumer.py /

#Execute a python file
CMD python consumer.py

