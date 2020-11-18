FROM nethacker/ubuntu-18-04-python-3:python-3.7.3
COPY requirements.txt /root/
RUN pip3 install -r /root/requirements.txt && useradd -m ubuntu && mkdir /home/ubuntu/logs
RUN pip3 install git+https://github.com/mongomock/mongomock.git@26058e8c4c93bc014c6b05078deb797baaf7b725
ENV HOME=/home/ubuntu
USER ubuntu
COPY app_server.py /home/ubuntu/
COPY src /home/ubuntu/src
COPY tests /home/ubuntu/tests
WORKDIR /home/ubuntu/
EXPOSE 8000
CMD ["gunicorn", "-c", "src/conf/gunicorn.py", "app_server:app"]
