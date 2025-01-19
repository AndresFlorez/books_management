# Build stage
FROM python:3.10-buster AS build

WORKDIR /app

COPY . .

RUN apt-get -y update && \
    apt-get --no-install-recommends install -y gettext && \
    apt-get clean

# Install SQLite 3.35.5 from source
RUN wget https://www.sqlite.org/2021/sqlite-autoconf-3350500.tar.gz && \
    tar xvfz sqlite-autoconf-3350500.tar.gz && \
    cd sqlite-autoconf-3350500 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3350500 sqlite-autoconf-3350500.tar.gz
# Ensure the new SQLite version is used
ENV LD_LIBRARY_PATH="/usr/local/lib"

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Runtime stage
# Expose the Django port
EXPOSE 8000

# Run Django’s development server
# CMD ["gunicorn", "app.wsgi:application", "-c", "gunicorn.conf.py"]
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
