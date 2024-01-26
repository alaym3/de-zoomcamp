#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # filename to save
    file_name = "yellow_tripdata_2021-01.parquet"

    # actually download the file from the url
    os.system(f"wget {url} -O {file_name}")
    df = pd.read_parquet(file_name)

    print("data loaded")
    # correct datatypes
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    # engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
    engine.connect()

    # just upload the schema
    df.head(0).to_sql(con=engine, name=table_name, if_exists="replace")
    print("Schema uploaded")

    print(f"Length of df... {len(df)}")

    df.to_sql(con=engine, name=table_name, if_exists="append")
    print("Data appended")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest parquet data to postgres")

    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host name for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--table_name", help="table name for postgres")
    parser.add_argument("--url", help="url for parquet file")

    args = parser.parse_args()
    main(args)
