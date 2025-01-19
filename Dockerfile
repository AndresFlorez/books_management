# Build stage
FROM python:3.10-buster AS build

WORKDIR /app

COPY . .

RUN apt-get -y update && \
    apt-get --no-install-recommends install -y gettext && \
    apt-get clean

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Runtime stage
# Expose the Django port
EXPOSE 8000

# Run Django’s development server
# CMD ["gunicorn", "app.wsgi:application", "-c", "gunicorn.conf.py"]
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
