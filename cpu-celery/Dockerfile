FROM python:3.9

LABEL maintainer="Otabek Olimjonov <bekdevs01@gmail.com>"

COPY ./ /main
WORKDIR /main

RUN pip install cmake 

RUN pip install -r /main/requirements.txt


ENTRYPOINT celery -A main worker -Q cpu_task -n cpu_worker@%h -l info