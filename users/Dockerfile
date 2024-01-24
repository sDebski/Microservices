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
# HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/core/health/ || exit 1
# RUN chmod +x /app/entrypoint.sh