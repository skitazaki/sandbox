FROM phusion/baseimage:0.9.13
MAINTAINER Shigeru Kitazaki <skitazaki@gmail.com>

ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN apt-get update

# `python3-pip` depends on `python3-devel`.
RUN apt-get install -y python3-pip nginx
RUN apt-get install -y python3-psycopg2

# Basic environment setup.
RUN locale-gen  en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Following instructions are based on `passenger-docker` image.
# see <https://github.com/phusion/passenger-docker> for the original.

# Add init script under runit.
RUN mkdir /etc/service/dashboard
ADD runtime/dashboard /etc/service/dashboard/run

## Create a user for the web app.
RUN addgroup --gid 9999 app
RUN adduser --uid 9999 --gid 9999 --disabled-password --gecos "Application" app
RUN usermod -L app
RUN gpasswd -a app sudo

# Remove this later.
ADD sshkey.pub /tmp/sshkey.pub

## Install SSH public key for "app" user.
USER app
RUN mkdir -p /home/app/.ssh
RUN cat /tmp/sshkey.pub >> /home/app/.ssh/authorized_keys
RUN chmod 700 /home/app/.ssh
RUN chmod 600 /home/app/.ssh/authorized_keys

USER root

## Install SSH public key for "root" user.
RUN mkdir -p /root/.ssh
RUN cat /tmp/sshkey.pub >> /root/.ssh/authorized_keys
RUN chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/authorized_keys

RUN rm -f /tmp/sshkey.pub
ADD runtime/sshd_config /etc/ssh/sshd_config

# Setup Python runtime environment.
ADD requirements.txt /env/requirements.txt
RUN pip3 install -r /env/requirements.txt
RUN pip3 install gunicorn
ADD src /app

## Setup Django app for production.
RUN sed -i 's:^DEBUG = True$:DEBUG = False:g' /app/dashboard/settings.py
ADD secret_key.txt /env/.secret_key.txt

## Copy admin and rest framework assets.
RUN sed -i 's:/tmp/static:/usr/share/nginx/html/static:g' /app/dashboard/settings.py
RUN cd /app && python3 manage.py collectstatic --noinput

## Install Nginx runit service.
RUN mkdir /etc/service/nginx
ADD runtime/nginx /etc/service/nginx/run
ADD runtime/nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/service/nginx-log-forwarder
ADD runtime/nginx-log-forwarder /etc/service/nginx-log-forwarder/run

## Put client side files.
ADD client/dist /usr/share/nginx/html

# Expose ports.
EXPOSE 80

# Cleanup when all done well.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Define default command.
CMD ["/sbin/my_init"]

