FROM python:3-alpine
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH /usr/src/app
CMD ["/app/src/app/app.py"]