FROM nethacker/ubuntu-18-04-python-3:python-3.7.3
COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt && useradd -m ubuntu && mkdir /home/ubuntu/logs
ENV HOME=/home/ubuntu
USER ubuntu
COPY app_server.py /home/ubuntu/
COPY src /home/ubuntu/src
COPY tests /home/ubuntu/tests
WORKDIR /home/ubuntu/
EXPOSE 8000
CMD ["gunicorn", "-c", "src/conf/gunicorn.py", "app_server:app"]
