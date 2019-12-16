FROM python:3.6.7-alpine
RUN apk add --no-cache git \
    build-base
RUN mkdir -p /opt/project
WORKDIR /opt/project
ADD requirements.txt /opt/project
RUN pip install -U pip
RUN pip install -r requirements.txt
ADD . /opt/project
CMD ["python", "main.py" ]