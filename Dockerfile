FROM python:3
RUN pip3 install pygame
RUN pip3 install scikit-neuralnetwork
ADD . /blocks
WORKDIR /blocks
CMD [ "python3", "-u", "./main.py" ]
