FROM python:3.12-slim-bookworm

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get upgrade \
  && apt-get install -y --no-install-recommends \
	build-essential \
	libpq-dev \	
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /app

COPY ./entrypoint.sh /

RUN chmod +x /entrypoint.sh

RUN mkdir -p statics \
	&& chown -R appuser:appgroup statics \
	&& chmod -R 755 statics

USER appuser

ENTRYPOINT ["sh","/entrypoint.sh"]
