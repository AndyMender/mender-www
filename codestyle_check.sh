#!/bin/bash

python -m pycodestyle --show-source --show-pep8 *.py libs/*.py tests/*.py
python -m isort -rc --diff *.py libs/*.py tests/*.py
python -m pytest -rs