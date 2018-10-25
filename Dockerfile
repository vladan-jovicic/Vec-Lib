FROM ubuntu:16.04

MAINTAINER Vladan "admin@jovicic.cf"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get install --assume-yes -y libsm6 libxext6
RUN apt-get install --assume-yes libglib2.0-0
RUN apt-get install --assume-yes -y libxrender-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
