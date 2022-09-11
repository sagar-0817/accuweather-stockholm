# Import all necessary libraries
import requests
import logging
import os
import datetime
import pandas as pd
from fastavro import writer, reader, parse_schema

# Set the severity of the logger to 'DEBUG'
logging.basicConfig(level=logging.DEBUG)

# Get the environment variable 'API_KEY'
api_key = os.environ.get("ACCUWEATHER_API_KEY")

# Set parameters to be passed along with the request
params = {
    'apikey': api_key
}

# Send a 'GET' request to the endpoint
response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/314929/historical/24', params=params)

# Exit the execution of the script if the status code of the response is not 200 (success)
if response.status_code != 200:
    logging.info(f"Invalid status code : {response.status_code}")
    exit()

# Get the response as a JSON object
data_24_hours_raw = response.json()

# Initialise an empty list to store processed records
data_24_hours_processed = list()

for record_raw in data_24_hours_raw:
  # Initialise an empty dictionary to store each processed record
  record_processed = dict()

  # Extract data from raw record

  observation_time_str = record_raw.get("LocalObservationDateTime")
  observation_time_datetime = datetime.datetime.strptime(observation_time_str, "%Y-%m-%dT%H:%M:%S%z")
  record_processed["local_observation_date_time"] = observation_time_str
  record_processed["year"] = observation_time_datetime.year
  record_processed["month"] = observation_time_datetime.month
  record_processed["day"] = observation_time_datetime.day
  record_processed["hour"] = observation_time_datetime.hour

  record_processed["weather_text"] = record_raw.get("WeatherText")
  record_processed["has_precipitation"] = record_raw.get("HasPrecipitation")
  record_processed["precipitation_type"] = record_raw.get("PrecipitationType") if record_raw.get("PrecipitationType") else ""
  record_processed["is_day_time"] = record_raw.get("IsDayTime")
  record_processed["temperature_celsius"] = record_raw.get("Temperature").get("Metric").get("Value")
  record_processed["temperature_fahrenheit"] = record_raw.get("Temperature").get("Imperial").get("Value")

  # Append processed record
  data_24_hours_processed.append(record_processed)

# Log the sample data 
logging.info(f"Sample data\n{pd.DataFrame(data_24_hours_processed).head(5)}")

# 1. Define the schema for the avro file
schema = {
    'doc': 'Weather report -  24 hours',
    'name': 'Weather',
    'namespace': 'stockholm',
    'type': 'record',
    'fields': [
        {'name': 'local_observation_date_time', 'type': 'string'},
        {'name': 'year', 'type': 'int'},
        {'name': 'month', 'type': 'int'},
        {'name': 'day', 'type': 'int'},
        {'name': 'hour', 'type': 'int'},
        {'name': 'weather_text', 'type': 'string'},
        {'name': 'has_precipitation', 'type': 'boolean'},
        {'name': 'precipitation_type', 'type': 'string'},
        {'name': 'is_day_time', 'type': 'boolean'},
        {'name': 'temperature_celsius', 'type': 'float'},
        {'name': 'temperature_fahrenheit', 'type': 'float'}
    ]
}

parsed_schema = parse_schema(schema)

# Write the data to an avro file
with open('stockholm-weather.avro', 'ab+') as f:
    writer(f, parsed_schema, data_24_hours_processed)


# Initialise an empty list to store the records read from the saved avro file
avro_records = []

# Read data from the saved avro file
with open('stockholm-weather.avro', 'rb') as fo:
    avro_reader = reader(fo)
    for record in avro_reader:
        avro_records.append(record)

# Log the number of records in the avro file (should be in multiples of 24)
logging.info(f"The number of records in the avro file is: {len(avro_records)}")
