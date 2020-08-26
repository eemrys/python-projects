FROM python:3.7

WORKDIR /test
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY ip_validator.py test_validator.py ./