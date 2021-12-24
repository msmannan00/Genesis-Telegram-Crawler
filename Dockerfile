FROM python:3.8

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

EXPOSE 5000
EXPOSE 27017
COPY . .
CMD ["flask", "run"]
