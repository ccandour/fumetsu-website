# Start with building a python app
FROM python:3.13 AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project source code
COPY ./django_site /django_site

# Set work directory
WORKDIR /django_site

# Set PYTHONPATH
ENV PYTHONPATH=/django_site

# Execute entrypoint shell script
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]