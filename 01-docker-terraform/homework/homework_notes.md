### Q 1.

      --rm                             Automatically remove the container when it exits

### Q 2

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list

docker run -it --entrypoint=bash python:3.9

wheel 0.42.0

Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0

## prep postgres

do all the steps from the video except use different datasets.
upload the data into the postgres.

Run Postgres and load data as shown in the videos We'll use the green taxi trips from September 2019:

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

You will also need the dataset with zones:

wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

-- full thing

step 1.

docker network create week1-pg-network


docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="week1_hw"  \
  -v "$(pwd)"/week1_hw_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=week1-pg-network \
  --name=week1-pg-database \
postgres:13


ingest is already good.


docker build . -t taxi_hw:v1

docker run -it \
  --network=week1-pg-network \
  taxi_hw:v1 \
    --user=root \
    --password=root \
    --host=week1-pg-database \
    --port=5432 \
    --db=week1_hw \
    --taxi_trips_table_name=taxi_trips \
    --taxi_zones_table_name=taxi_zones \
    --taxi_trips_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz" \
    --taxi_zones_url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

THIS WORKED





Question 3. Count records
How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that lpep_pickup_datetime and lpep_dropoff_datetime columns are in the format timestamp (date and hour+min+sec) and not in date.

15767
15612 -- right, but some data is incorrect lol should be 15600
15859
89009

select count(*) from taxi_trips
where
lpep_pickup_datetime >= '2019-09-18 00:00:00' and lpep_pickup_datetime < '2019-09-19 00:00:00'
and lpep_dropoff_datetime >= '2019-09-18 00:00:00'and lpep_dropoff_datetime < '2019-09-19 00:00:00'

Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance.

2019-09-18
2019-09-16
2019-09-26 -- correct, 341.64
2019-09-21

SELECT
	date_trunc('day', lpep_pickup_datetime) AS date_trip,
	max(trip_distance) AS max_trip_per_day
FROM
	taxi_trips
GROUP BY
	date_trip
ORDER BY
	max_trip_per_day DESC;


Question 5. Three biggest pick up Boroughs
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

"Brooklyn" "Manhattan" "Queens" --> correct
"Bronx" "Brooklyn" "Manhattan"
"Bronx" "Manhattan" "Queens"
"Brooklyn" "Queens" "Staten Island"

SELECT
	zones. "Borough",
	sum(trips. "total_amount") AS total_amount
FROM
	taxi_trips trips
	INNER JOIN taxi_zones zones ON trips. "PULocationID" = zones. "LocationID"
WHERE
	date_trunc('day', lpep_pickup_datetime) = '2019-09-18 00:00:00'
GROUP BY
	zones. "Borough"
HAVING
	zones. "Borough" != 'Unknown'
ORDER BY
	total_amount DESC
LIMIT 10;

Question 6. Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's tip , not trip

Central Park
Jamaica
JFK Airport --> correct, 62.31
Long Island City/Queens Plaza

SELECT
	date_trunc('month', lpep_pickup_datetime),
	pickup_zones. "Zone" AS pu_zone,
	dropoff_zones. "Zone" AS do_zone,
	trips.tip_amount
FROM
	taxi_trips trips
	INNER JOIN taxi_zones pickup_zones ON trips. "PULocationID" = pickup_zones. "LocationID"
	INNER JOIN taxi_zones dropoff_zones ON trips. "DOLocationID" = dropoff_zones. "LocationID"
WHERE
	date_trunc('month', lpep_pickup_datetime) = '2019-09-01' -- 00:00:00'
	AND pickup_zones. "Zone" = 'Astoria'
ORDER BY
	tip_amount DESC;




for terraform in the vm: 
config gcloud cli credentials
export GOOGLE_APPLICATION_CREDENTIALS=~/.keys/creds.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS


and remove creds from main.


terraform apply :

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_storage_bucket.demo-bucket: Creation complete after 3s [id=atomic-airship-410619-terra-bucket]
google_bigquery_dataset.demo_dataset: Creation complete after 3s [id=projects/atomic-airship-410619/datasets/demo_dataset]

