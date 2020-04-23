ARG PYTHON_VERSION=3.8.2-slim-buster

FROM python:${PYTHON_VERSION}

MAINTAINER Reda Ouled

ENV PYTHONUNBUFFERED 1
ENV TZ Europ/Paris

WORKDIR /var/www/ipssi.project.web

COPY ./src .
COPY ./docker/system/bashrc /root/.bashrc

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
        curl \
        sudo \
        wget \
        vim \
        lsof \
    && pip install -U pip \
    && pip install pip-tools \
    && pip install --upgrade pip \
	\
	&& rm -rf /var/lib/apt/lists/* \
    && echo "$(head -n 1 /etc/hosts) $(echo -n 1 /etc/hosts | awk '{print $2}').localdomain" >> /etc/hosts \
    && rm /etc/localtime \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && "date"
