FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/




EXPOSE 8000
# CMD ["gunicorn", "bookinghotel.wsgi:application", "--bind", "0.0.0.0:8000"]
