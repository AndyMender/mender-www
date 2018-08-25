#!/bin/bash

python -m pycodestyle *.py
python -m isort *.py
# python -m pytest tests