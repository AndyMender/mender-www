#!/bin/bash

python -m pycodestyle --show-source --show-pep8 *.py libs/*.py
python -m isort *.py libs/*.py
# python -m pytest tests