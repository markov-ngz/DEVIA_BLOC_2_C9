FROM python:3.11.9-bookworm

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get upgrade -y \
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

# ugly multiple layers, as a bug occured on windows building the image  zzzzz
RUN mkdir -p statics 
RUN mkdir -p hf_cache 
RUN chown -R appuser:appgroup statics
RUN chmod -R 755 statics
RUN chown -R appuser:appgroup hf_cache 
RUN chmod -R 755 hf_cache

USER appuser

ENTRYPOINT ["sh","/entrypoint.sh"]
