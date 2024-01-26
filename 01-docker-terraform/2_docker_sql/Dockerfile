FROM python:3.9


RUN apt-get install wget
RUN pip install pandas==1.5.3 SQLAlchemy==1.4.51 psycopg2 fastparquet


WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]