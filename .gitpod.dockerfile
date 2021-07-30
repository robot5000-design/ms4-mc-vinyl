FROM gitpod/workspace-full
FROM gitpod/workspace-postgres

# Docker build does not rebuild an image when a base image is changed, increase this counter to trigger it.
ENV TRIGGER_REBUILD=1
# Install PostgreSQL
RUN sudo install-packages postgresql-12 postgresql-contrib-12

# Setup PostgreSQL server for user gitpod
ENV PATH="$PATH:/usr/lib/postgresql/12/bin"
ENV PGDATA="/workspace/.pgsql/data"
RUN mkdir -p ~/.pg_ctl/bin ~/.pg_ctl/sockets \
 && printf '#!/bin/bash\n[ ! -d $PGDATA ] && mkdir -p $PGDATA && initdb -D $PGDATA\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" start\n' > ~/.pg_ctl/bin/pg_start \
 && printf '#!/bin/bash\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" stop\n' > ~/.pg_ctl/bin/pg_stop \
 && chmod +x ~/.pg_ctl/bin/*
ENV PATH="$PATH:$HOME/.pg_ctl/bin"
ENV DATABASE_URL="postgresql://gitpod@localhost"
ENV PGHOSTADDR="127.0.0.1"
ENV PGDATABASE="postgres"

# This is a bit of a hack. At the moment we have no means of starting background
# tasks from a Dockerfile. This workaround checks, on each bashrc eval, if the
# PostgreSQL server is running, and if not starts it.
RUN printf "\n# Auto-start PostgreSQL server.\n[[ \$(pg_ctl status | grep PID) ]] || pg_start > /dev/null\n" >> ~/.bashrc


USER root
# Setup Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# Setup MongoDB and MySQL
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 20691eec35216c63caf66ce1656408e390cfb1f5 && \
    echo "deb http://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list  && \
    apt-get update -y  && \
    touch /etc/init.d/mongod  && \
    apt-get -y install mongodb-org-shell -y  && \
    apt-get -y install links  && \
    apt-get install -y mysql-server && \
    apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/* && \
    mkdir /var/run/mysqld && \
    chown -R gitpod:gitpod /etc/mysql /var/run/mysqld /var/log/mysql /var/lib/mysql /var/lib/mysql-files /var/lib/mysql-keyring /var/lib/mysql-upgrade /home/gitpod/.cache/heroku/ && \
    pip3 install flake8 flake8-flask flake8-django

# Create our own config files

COPY .vscode/mysql.cnf /etc/mysql/mysql.conf.d/mysqld.cnf

COPY .vscode/client.cnf /etc/mysql/mysql.conf.d/client.cnf

COPY .vscode/start_mysql.sh /etc/mysql/mysql-bashrc-launch.sh

USER gitpod

# Start MySQL when we log in

RUN echo ". /etc/mysql/mysql-bashrc-launch.sh" >> ~/.bashrc

# Local environment variables
# C9USER is temporary to allow the MySQL Gist to run
ENV C9_USER="gitpod"
ENV PORT="8080"
ENV IP="0.0.0.0"
ENV C9_HOSTNAME="localhost"

USER root
# Switch back to root to allow IDE to load