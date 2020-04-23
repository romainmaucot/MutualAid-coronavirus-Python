ARG POSTGRES_VERSION

FROM postgres:${POSTGRES_VERSION}

ENV TZ Europ/Paris

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone \
  && "date"

