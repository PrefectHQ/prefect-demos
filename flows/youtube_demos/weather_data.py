from prefect import flow, task, get_run_logger
import requests
import pandas as pd



@task
def get_weather_data():
    lat = 42.36626947261866
    lon = -71.09014952641706
    key = 'key'
    part = 'minutely,hourly,daily'

    request_string = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}'

    response = requests.get(request_string)
    print(response.json())