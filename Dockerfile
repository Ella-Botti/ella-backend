FROM ubuntu:18.04
WORKDIR /usr/src/app
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install sudo
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install python-telegram-bot
RUN pip3 install python-dotenv
RUN apt-get -y install python3-psycopg2
#RUN apt-get -y install postgresql
#RUN service postgresql start;sudo -u postgres createdb root;sudo -u postgres createuser root;psql -U root -d root -f assa.sql
#RUN sudo -u postgres createdb root
#RUN sudo -u postgres createuser root
#RUN psql -U root -d assa -f assa.sql

ENTRYPOINT ["python3", "ella_bot.py"]