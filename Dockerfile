FROM python:3.6

RUN apt-get update

RUN apt-get install -y software-properties-common

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 9005

ENTRYPOINT ["python3"]

CMD ["-m", "application"]
