FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "requirements installed"

CMD ["tail", "-f", "/dev/null"]