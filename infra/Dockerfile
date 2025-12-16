FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app
COPY docs/VERSION /app/docs/VERSION
COPY assets/logo /tmp/assets/logo

RUN mkdir -p app/static/logo \
    && cp -r /tmp/assets/logo/. app/static/logo/ \
    && rm -rf /tmp/assets

EXPOSE 8000

CMD ["python", "wsgi.py"]
