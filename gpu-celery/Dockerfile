FROM nvcr.io/nvidia/tensorflow 

LABEL maintainer="Otabek Olimjonov <bekdevs01@gmail.com>"

COPY ./ /main
WORKDIR /main

RUN pip install -r /main/requirements.txt

ENTRYPOINT celery -A main worker -Q gpu_task -n gpu_worker@%h -P solo -l info 