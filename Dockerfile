FROM python:3.8-slim
LABEL maintainer="u6k.apps@gmail.com"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        tor \
        privoxy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -U pip && \
    pip install pipenv

RUN echo 'forward-socks5 / localhost:9050 .' >/etc/privoxy/config

WORKDIR /var/myapp
VOLUME /var/myapp

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --dev --system

CMD ["scrapy", "-h"]
