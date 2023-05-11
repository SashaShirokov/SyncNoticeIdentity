FROM python:3.10-slim-buster

WORKDIR /SyncIdentity

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y git \
  && apt-get install -y cron

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

COPY ./id_ed25519 /root/.ssh/id_ed25519
COPY ./config /root/.ssh/config

RUN touch /var/log/cron.log

#RUN (crontab -l ; echo "*/30 * * * * cd /SyncIdentity/identity-server-poc && git pull >> /var/log/cron.log && git push --porcelain >> /var/log/cron.log && echo '' >> /var/log/cron.log") | crontab

#RUN (crontab -l ; echo "*/1 * * * * cd /SyncIdentity/notification/notice && python main.py >> /var/log/cron.log") | crontab

RUN (crontab -l ; echo "*/1 * * * * echo 'Hello' >> /var/log/cron.log && cd /SyncIdentity/notification/notice && /usr/local/bin/python3.10 main.py >> /var/log/cron.log") | crontab


RUN chmod 600 /root/.ssh/id_ed25519 && \
    ssh-keyscan -t ed25519 -H github.com >> /root/.ssh/known_hosts && \
    ssh-keyscan -t ed25519 -H gitlab.com >> /root/.ssh/known_hosts

COPY . /SyncIdentity

CMD cron && tail -f /var/log/cron.log
