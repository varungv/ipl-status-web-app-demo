FROM python:3.8-alpine # because it is the latest and lightest version of python

WORKDIR /app

# Routine image updates
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Copying the entire source folder, not to mention the DBSqlite3 also. To avoid creating the DB every time.
COPY . .

# installing dependencies
RUN pip install -r requirements.txt

# add and run as non-root user
# RUN adduser -D myuser
# USER myuser

# run gunicorn
CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT