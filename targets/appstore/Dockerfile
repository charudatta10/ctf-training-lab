FROM python:3.11-alpine

WORKDIR /www

# It serves whatever is mounted into /www (see compose.yml).
CMD ["python", "-m", "http.server", "8001", "--directory", "/www"]