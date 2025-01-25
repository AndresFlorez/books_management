# Build stage
FROM python:3.12-slim AS build

WORKDIR /app

COPY . .

RUN apt-get -y update && \
    apt-get --no-install-recommends install -y gettext && \
    apt-get clean

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Runtime stage
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--", "/entrypoint.sh"]

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--config", "gunicorn.conf.py", "--timeout", "30"]
