FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libssl-dev
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 3306
CMD [ "python3", "app.py" ]