FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements/ /code/
RUN pip install -r requirements/production.txt
COPY . /code/
