FROM python:2.7

# dependencies
RUN apt-get install -y curl
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.32.0/install.sh | bash

# pdb-vis
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY bower.json /usr/src/app/
COPY .bowerrc /usr/src/app/
RUN . ~/.nvm/nvm.sh && nvm install v4.4.0 && \
    npm install -g bower && bower install --allow-root

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# settings
EXPOSE 6015
