FROM python:3.10

COPY . /app

WORKDIR /app

# satisfy Python requirements
RUN python -m pip install -r requirements.txt

# check code style, import ordering and run pytest tests
RUN ./codestyle_check.sh

# NOTE: the health check is run periodically after container UP to validate if the app is available
# NOTE2: health checks can be implemented at a higher level, for instance, on the load balancer or Kubernetes Deployment object
HEALTHCHECK --interval=15s --timeout=60s --start-period=5s --retries=3 CMD curl -f http://localhost:8000 || exit 1

# start server
CMD ["python", "main.py"]
