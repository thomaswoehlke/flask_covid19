#!/usr/bin/env bash

## https://www.rabbitmq.com/admin-guide.html
#
## https://www.rabbitmq.com/admin-guide.html#access-control

sudo systemctl restart rabbitmq-server.service

sudo rabbitmqctl add_user flask_covid19 flask_covid19pwd
sudo rabbitmqctl add_vhost tw-thinkpad
sudo rabbitmqctl set_user_tags flask_covid19 flask_covid19_celery
sudo rabbitmqctl set_permissions -p tw-thinkpad flask_covid19 ".*" ".*" ".*"

sudo rabbitmqctl status
