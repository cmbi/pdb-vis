FROM python:2.7-onbuild

RUN apt-get install -y curl
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.32.0/install.sh | bash

RUN . ~/.nvm/nvm.sh ; nvm install v4.4.0 ; npm install -g bower ; bower install --allow-root

WORKDIR /usr/src/app
EXPOSE 8015
