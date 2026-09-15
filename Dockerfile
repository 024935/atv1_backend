FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_PORT=3589
EXPOSE 3589

CMD ["sh", "-c", "python run.py"]
