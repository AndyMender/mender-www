FROM python:3.10

COPY . /app

WORKDIR /app

# satisfy Python requirements
RUN python -m pip install -r requirements.txt

# check code style, import ordering and run pytest tests
RUN ./codestyle_check.sh

# start server
CMD ["python", "main.py"]
