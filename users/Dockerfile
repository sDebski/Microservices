FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

RUN apt-get update; \
	apt-get install -y --no-install-recommends \
		netcat \
        libpq-dev \
	;

COPY . .
ENTRYPOINT [ "sh", "./entrypoint.sh" ]