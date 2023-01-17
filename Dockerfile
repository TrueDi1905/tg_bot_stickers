FROM python:3.9.16-slim-bullseye
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app/bot
CMD ["python", "main.py"]
