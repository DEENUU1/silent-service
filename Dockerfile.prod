FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
COPY .env /app/

RUN pip install -r requirements.txt

RUN addgroup --system app && adduser --system --group app

COPY . /app/

RUN mkdir -p /app/staticfiles

RUN python manage.py collectstatic --noinput