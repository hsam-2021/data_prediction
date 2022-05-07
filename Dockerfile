FROM python:3.9
ADD . /data_prediction
WORKDIR /data_prediction
RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
#EXPOSE 5000
CMD ["python","-u", "server/app.py"]
