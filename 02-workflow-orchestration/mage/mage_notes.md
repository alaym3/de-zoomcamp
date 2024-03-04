- to get new mage version
  pull mageai/makeai:latest

- clone the mageai quickstart repo
  https://github.com/mage-ai/mage-zoomcamp
  docker-compose build - to build
  docker-compose up - to run it locally
  it is available in http://localhost:6789/ - that's the port mage is on. postgres is 5432 as usual.

- ETL: api to postgres
- this is all happening within the mage interface on http://localhost:6789/

new batch pipeline
change name - api_to_postgres
new data loader: load_api_data

in extract py script:
set URL
set dtypes
set dattimes as a list of dates to parse

    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }

    parse_dates = ['tpep_pickup_datetime','tpep_dropoff_datetime']

    return pd.read_csv(url, sep=",", compression='gzip',dtype=taxi_dtypes, parse_dates=parse_dates)

then we run the extract code.
scroll down to see the df.

then add transform code

first basic:

@transformer
def transform(data, \*args, \*\*kwargs):
print(f"Preprocessing: rows with 0 passengers: {data['passenger_count'].isin([0]).sum()}")

    return data[data['passenger_count'>0]]

basic test to confirm the 0 passenger rides are removed
@test
def test_output(output, \*args) -> None:
"""
Template code for testing the output of the block.
"""
assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers.'

- add data exporter, to get the transformed data to postgres. choose python to postgres.

change io_config yaml file and add 'dev' config at the bottom, to make export run. it's in 2.2.3 video instead.

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_postgres(df: DataFrame, \*\*kwargs) -> None:
"""
Template for exporting data to a PostgreSQL database.
Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_cab_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )

then access postgres locally like usual; the data is there.

- then we can do a sql data loader just to check if it;'s there, without needing to open postgres locally.
  -- choose postgres, and dev profile

-- ALL OF THE FILES ARE COMING BACK TO VSCODE WHILE IT'S UPDATING IN LOCALHOST ON THE WEB UI!!!!

- gcp setup
  make a bucket
  make a service account
  make new key, put the json file in the repo
  authenticate inside mage -
  io_config - service account. paste the json payload, or use the service acount key filepath.
- we will use filepath.

  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/atomic-airship-410619-7f4a4593c192.json"

then add a sql loader script to check bigquery conn plus default profile.

- the example pipeliine has a full set for titanic. if we run it....
  titanic_clean.csv is saved in our local files now.. and we can upload it into the gcp bucket.

-- docker-compose down will stop the containers, but all the work is maintained due to the volume.

### now API to GCP

bucket mage-zoomcamp-aam in project atomic-airship-410619

setting up GCP to allow mage to read and write data.
we piut titanic_clean inside of it, now let's create a data loader from python to load data from the bucket and test that it works.

- just put the bucket name and the object name,

- create a new pipeline for this to make it cleaner.
- we can just drag the old code load_api_data.py into our new pipeline. and the transformer. then drag and attach them.
- now we send to gcp by adding a data exporter from pythoon to gcs
- all we have to do is put the bucket name and the object, with whatever file format we want

- we can do a more legit way of loading to gcp by adding python no template data exporter.
- make it connected to the transformer so tjhat it runs in parallel with the other exporter to gcs

  - define creds manually
  - use pyarrow to partition the dataset

  - imports
  - tell pyarrow where our credentials are.
  - open terminal, ls -la to copy the path in home/src of the json creds file
  - add bucket name, project id, and table name
  - then pyarrow handles partitioning
  - set the root path as the bucket name / table name

partitioning by date is a helpful pattern
first we need to create a date column from the unix timestamp

- read df into pyarrow table
- make gcs file object
- then write to dataset

import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/atomic-airship-410619-7f4a4593c192.json"

bucket_name = "mage-zoomcamp-aam"
project_id = "atomic-airship-410619"

table_name = "nyc_taxi_data"

root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data(data, \*args, \*\*kwargs):
data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['tpep_pickup_date'],
        filesystem=gcs
    )

- now this runs datasets into multiple parquet datafiles to make it speed up the reading and writing, and loading. now we have a new parquet file for each date.
- more efficient from a query standpoint to only load data from the dates that we need instead of loading all.
- pyarrow abstracts away the chunking logic. so we dont need to iterate and do io operations. so it does that for us and makes it easier.
- so now we end with our partitioned dataset inside a foler in gcs, instead of in 1 file.

--- 2.2.5: writing our data to bigquery. traditional.. load data, stage in file storage, and import to database

- new batch pipeline.
- python data loader from gcs
- unpartitioned file for this demo.
- run to load the dataset
- now add a transformation
- a best practice is to standardize the column names and clean them up - remove space and make underscore, and lowercase all.

@transformer
def transform(data, \*args, \*\*kwargs):
data.columns = (data.columns
.str.replace(' ','\_')
.str.lower()
)

    return data

now add a sql exporter. add bigquery default connection. specify schema and table.

- set the ny_taxi database and the yellow_cab_data as the table.
- you can select diretly from dataframes.. df_1 is returned from the transformer.
- select \* from {{ df_1 }} will immediately export that data to the table!!!!! wow what??? that is so simple lol.
- it saves a staging table with all the data that has a name of dev + pipeline + transformation
- then it saves a table with the actual table name we specified

scheduling

- triggers: they schedule workflows
- based on schedule, event, or api
- add schedule based one
- then enable it, and i's active

## 2.2.6 parameterized executions

- incremental daily load - save each day's worth of data into a separate file
- load to gcp example - clone it.
- editing blocks impact the blocks everywhere.
  - so we will replicate the block
- we can use kwargs to get the execution date.
- save the date in the filepath as the name
- so we could schedule this to run everyday and it would save to the path for the day.
- you can set variables within the pipeline (right hand side click variables)
- setting a date filepath kwarg is not enough; you still need to schedule it everyday and update the data loaading or trasnsform block so that is only pulls in the data from the last day or timeframe.

## 2.2.6: backfills

- if we have lost our data, or have some missing data, we need to backfill to ensure data consistency
- in other dags we need to do bulk calls
- in mage it's very easy to replicate or retrieve lost data
- backfills tab
- add a date and time window, and set the time window
  - e.g. 7 day timerange, by day, 1 change.

## 2.2.7: deploying mage with terraform on gcp

- prereqs: tf, gcloud gli, google cloud permissions, mage tf templates
- gcp permissions: artifact reg read, write, gc run dev, etc.
  - iam admin
- gcloud auth list shows list of credentialed accounts
  To set the active account, run:
  $ gcloud config set account `ACCOUNT`
- gcloud storage ls lists all buckets you have access to
- we deploy it via cloudrun
- need to whitelist the ip addres to access it
- it will persist on google cloud and will store the files
- if the project is started and stopped then the files will be there
- as long as its running, it will be continuously deployed
- how do we get the stuff we built in here??
  - git sync - mage has a bunch
  - just push to git and set up syncing with mage

gcloud auth login
gcloud config set project atomic-airship-410619

git clone https://github.com/mage-ai/mage-ai-terraform-templates.git

figure out the right thing to do about deploying tf; lots of missing info

use creds json

Yes, I had to do multiple things to get it to run after cloning the template:

1. Fill in your variables and the path to the credentials .json
2. I had to manually activate multiple services in GCP
3. I also had to delete the service account and create a new one with the "owner" role as I got a bunch of permission denied errors.
