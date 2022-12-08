FROM python:3.9.6-alpine3.14

WORKDIR /app

RUN python -m pip install --upgrade pip 
RUN python -m pip install setuptools wheel
RUN apk add --update

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["python", "server.py"]
