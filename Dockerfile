FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /WebsiteISJ/
WORKDIR /WebsiteISJ/

COPY ./requirements.txt /WebsiteISJ/requirements.txt

RUN pip install -r requirements.txt

VOLUME /WebsiteISJ
