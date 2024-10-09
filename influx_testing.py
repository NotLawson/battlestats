import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

influx_token = "5w2KfrU5cAZeKyb1oQTnNWsZnidKw_HDs-ffm6jgFP865Is3p8nSc5vI8nI2pJOD_ERVj2VvVh5MtXTjFnO-lg=="
org = "battlestats"
url = "http://192.168.86.231:8086"

influx_client = influxdb_client.InfluxDBClient(url=url, token=influx_token, org=org)

bucket="stats"

write_api = influx_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="battlestats", record=point)
  time.sleep(1) # separate points by 1 second


query_api = influx_client.query_api()

query = """from(bucket: "stats")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="battlestats")

for table in tables:
  for record in table.records:
    print(record)



