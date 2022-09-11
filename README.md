# Accuweather - Stockholm

## Description
The purpose of the project is to:
- scrape the last 24 hours weather data of Stockholm from the [Accuweather](https://www.accuweather.com/) API
- store the weather data in an avro file


## Project Contents

- [main.py](https://github.com/sagar-0817/accuweather-stockholm/blob/main/main.py)
    - the python script scrapes the weather data, processes the raw data, appends the processed data to an avro file 
    - a detailed explanation of the script is mentioned as comments
- [requirements.txt](https://github.com/sagar-0817/accuweather-stockholm/blob/main/requirements.txt)
   - contains the packages required to run the script
- [.github/workflows/python-workflow.yaml](https://github.com/sagar-0817/accuweather-stockholm/blob/main/.github/workflows/python-workflow.yaml)
    - workflow to run the script on a daily basis as well as manually
    - any changes to the repository are automatically commited

- [stockholm-weather.avro](https://github.com/sagar-0817/accuweather-stockholm/blob/main/stockholm-weather.avro)
    - The output avro file containing the stockholm weather data

## Notes

- The script is scheduled to run every midnight (at 00:00 hours)
- The script can also be manually triggered ([Actions](https://github.com/sagar-0817/accuweather-stockholm/actions/workflows/python-workflow.yaml) tab)
- The API key required to scrape the data is stored as a secret called [ACCUWEATHER_API_KEY](https://github.com/sagar-0817/accuweather-stockholm/settings/secrets/actions)
- The scraped data is appended to the avro file. The number of records in the avro file will be in multiples of 24.
- After every run, the output file (stockholm-weather.avro) is appended with latest data.
- The changes to the output file are commited automatically.
