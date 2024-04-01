FROM python:3.12-alpine

EXPOSE 8000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

COPY . /app

RUN pip install -r ./requirements.txt

COPY ./launch.sh /app/launch.sh
RUN chmod +x /app/launch.sh

CMD ["/app/launch.sh"]
