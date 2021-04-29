#the starting image was previously ubuntu:18.04, however a python alpine image is smaller,
#meaning faster pulling and building, yay
#in addition, this lets us use pip out of the box.
FROM python:3.9.4-alpine3.13
WORKDIR /usr/src/app
COPY . .
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2
RUN pip3 install python-telegram-bot
RUN pip3 install python-dotenv

ENTRYPOINT ["python3", "-u", "ella_bot.py"]
