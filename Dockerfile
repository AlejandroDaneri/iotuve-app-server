FROM ubuntu:latest
RUN apt-get update && \
 apt-get install -y \
 build-essential \
 python3-pip \
 python3-dev

# working directory
WORKDIR /app

# copy current directory into the container
ADD . /app

RUN pip3 install -r requirements.txt
# make port 8000 available to the world outside
EXPOSE 8000
CMD ["gunicorn", "--config", "./conf/gunicorn_conf.py", "src:app"]