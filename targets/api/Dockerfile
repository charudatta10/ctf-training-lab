FROM python:3.11-alpine

WORKDIR /app

RUN pip install --no-cache-dir Flask==3.0.3

COPY app.py /app/app.py
COPY certs /app/certs

EXPOSE 3000 3443

USER nobody

CMD ["python", "app.py"]