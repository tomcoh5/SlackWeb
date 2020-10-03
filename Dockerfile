FROM ubuntu:16.04

WORKDIR /app

RUN apt-get update -y && \
    apt-get install python3 -y && apt-get install python3-pip -y && apt-get install  python3-dev -y
RUN apt-get install python-requests -y
RUN easy_install3 pip
COPY . /app

RUN pip3 install -r requirements.txt


ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
