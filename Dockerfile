FROM python:3.9

ENV FLASK_DEBUG=0
ENV PORT=5000

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /back
COPY . /back

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
