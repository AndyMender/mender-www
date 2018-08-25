FROM python:3.6

COPY . /app

WORKDIR /app

RUN python -m pip install -r requirements.txt

RUN ./codestyle_check.sh

CMD ["flask", "run"]
