FROM python:3.10-slim-buster

WORKDIR /SyncIdentity

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y git \
  && apt-get install -y cron \
  && apt-get install -y nano \
  && apt-get install -y vim \

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

COPY ./id_ed25519 /root/.ssh/id_ed25519
COPY ./config /root/.ssh/config

RUN touch /var/log/cron.log

# Sync identity project every half an hour
RUN (crontab -l ; echo "*/30 * * * * cd /SyncIdentity/identity-server-poc && git pull >> /var/log/cron.log && git push --porcelain >> /var/log/cron.log && echo '' >> /var/log/cron.log") | crontab

# Delete cron.log every Friday at 5pm
RUN (crontab -l ; echo "0 5 * * 5 rm -rf /var/log/cron.log") | crontab

# Scan identity projec at 10:00 on every day-of-week from Monday through Friday
RUN (crontab -l ; echo "0 10 * * * 1-5 cd /SyncIdentity && ./osv-scanner_1.3.2_linux_amd64 --lockfile ./identity-server-poc/poetry.lock > /SyncIdentity/scan.txt") | crontab

# Notify team at 10:05 on every day-of-week from Monday through Friday about scan result
RUN (crontab -l ; echo "5 10 * * 1-5 cd /SyncIdentity/notification/notice && /usr/local/bin/python3.10 main.py") | crontab


RUN chmod 600 /root/.ssh/id_ed25519 && \
    ssh-keyscan -t ed25519 -H github.com >> /root/.ssh/known_hosts && \
    ssh-keyscan -t ed25519 -H gitlab.com >> /root/.ssh/known_hosts

COPY . /SyncIdentity

CMD cron && tail -f /var/log/cron.log
