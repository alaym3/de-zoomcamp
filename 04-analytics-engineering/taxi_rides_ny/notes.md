## dbt

initialize project via cloud IDE in the specific subdirectory

use staging and core

it builds the views/tables inside bigquery in the dataset.

core should be table since it's faster for views for the end user
staging should be views

always use the test run variable so that doing tests will only process 100 rows and limit the costs on your data warehouse

to build up and downstream
dbt build --select +fact_trips+

and to make sure you run ALL and not limit
dbt build --select +fact_trips+ --vars '{'is_test_run': 'false'}'

## 6 - testing and documenting dbt models

we can put these in .yml files
out of the box

- unique
- not null
- accepted value
- foreign key from another table
  and you can make custom queries as tests
  they can send specific warnings if they fail
