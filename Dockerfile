FROM python:3.7-slim

EXPOSE 5000

COPY . /usr/src/app

RUN pip install Werkzeug[watchdog] colorama
RUN pip install /usr/src/app

CMD ["httpdummy", "--address=0.0.0.0"]
