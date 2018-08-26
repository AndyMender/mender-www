FROM python:3.6

COPY . /app

WORKDIR /app

# satisfy Python requirements
RUN python -m pip install -r requirements.txt

# install node.js and yarn
RUN apt update

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs

RUN npm install yarn -g

# install bulma (CSS framework)
RUN npm install bulma -g

# check code style, import ordering and run pytest tests
RUN ./codestyle_check.sh

# start server
CMD ["python", "main.py"]
