FROM python:3.10
ENV PYTHONUNBUFFERED=1
RUN mkdir /googleTrends
WORKDIR /googleTrends
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /googleTrends/
