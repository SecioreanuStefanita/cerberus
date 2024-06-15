FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y cron curl jq

RUN pip install flask

RUN pip install flask_cors

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY crontab.txt /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron

COPY config/routing_config.json /app/config/routing_config.json

RUN chmod +x /app/check_logs.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["cron", "-f"]
