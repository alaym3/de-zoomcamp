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
    taxi_trips_table_name = params.taxi_trips_table_name
    taxi_zones_table_name = params.taxi_zones_table_name
    taxi_trips_url = params.taxi_trips_url
    taxi_zones_url = params.taxi_zones_url


    # filename to save
    taxi_trips_file_name = "green_tripdata_2019-09.csv.gz"
    taxi_zones_file_name = "taxi+_zone_lookup.csv"

    # actually download the file from the url
    os.system(f"wget {taxi_trips_url} -O {taxi_trips_file_name}")
    taxi_trips_df = pd.read_csv(taxi_trips_file_name)
    print("Taxi trips datasets loaded")
    os.system(f"wget {taxi_zones_url} -O {taxi_zones_file_name}")
    taxi_zones_df = pd.read_csv(taxi_zones_file_name)
    print("Taxi zones datasets loaded")


    # correct datatypes
    taxi_trips_df["lpep_pickup_datetime"] = pd.to_datetime(taxi_trips_df["lpep_pickup_datetime"])
    taxi_trips_df["lpep_dropoff_datetime"] = pd.to_datetime(taxi_trips_df["lpep_dropoff_datetime"])

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    # engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
    engine.connect()

    # just upload the schema
    taxi_trips_df.head(0).to_sql(con=engine, name=taxi_trips_table_name, if_exists="replace")
    print("Taxi trips schema uploaded")

    taxi_zones_df.head(0).to_sql(con=engine, name=taxi_zones_table_name, if_exists="replace")
    print("Taxi zones schema uploaded")



    print(f"Length of taxi_trips_df... {len(taxi_trips_df)}")
    print(f"Length of taxi_zones_df... {len(taxi_zones_df)}")

    taxi_trips_df.to_sql(con=engine, name=taxi_trips_table_name, if_exists="append")
    print("Taxi trips data appended")

    taxi_zones_df.to_sql(con=engine, name=taxi_zones_table_name, if_exists="append")
    print("Taxi zones data appended")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest parquet data to postgres")

    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host name for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--taxi_trips_table_name", help="table name for postgres")
    parser.add_argument("--taxi_zones_table_name", help="table name for postgres")
    parser.add_argument("--taxi_trips_url", help="url for trips csv file")
    parser.add_argument("--taxi_zones_url", help="url for zones csv file")

    args = parser.parse_args()
    main(args)
