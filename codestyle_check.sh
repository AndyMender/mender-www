#!/bin/bash

python -m pycodestyle *.py libs/*.py
python -m isort *.py libs/*.py
# python -m pytest tests