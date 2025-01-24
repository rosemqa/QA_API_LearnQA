FROM python:3.12.3-alpine3.20

# update apk repo
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.20/main" >> /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories

# install packages (jdk, curl, tar, allure)
RUN apk update && \
    apk add openjdk21-jre curl tar && \
    curl -o allure-2.29.0.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.29.0/allure-commandline-2.29.0.tgz && \
    tar -zxvf allure-2.29.0.tgz -C /opt/ && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure && \
    rm allure-2.29.0.tgz

WORKDIR /test_project
COPY requirements.txt .
RUN pip install -r requirements.txt