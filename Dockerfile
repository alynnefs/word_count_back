FROM python:3.9

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /back
COPY . /back

EXPOSE 5000
ENTRYPOINT flask --app app/main run --host "0.0.0.0"
