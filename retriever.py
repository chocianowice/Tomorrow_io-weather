import requests
import json


def check_response_body(responseContent):
    # Checks if the structure of the response body has all required fields

    # data
    if not 'data' in responseContent:
        print('No data field in response json!')
        return False

    # timelines - existence, list type, length > 0
    if not 'timelines' in responseContent['data']:
        print('No timelines field in response json!')
        return False
    if not isinstance(responseContent['data']['timelines'], list):
        print('timelines field exists but is not a list in response json!')
        return False
    if not len(responseContent['data']['timelines']) > 0:
        print('timelines field exists but is not a list in response json!')
        return False

    # intervals - existence, list type, length > 0
    if not 'intervals' in responseContent['data']['timelines'][0]:
        print('No intervals field in response json!')
        return False
    if not isinstance(responseContent['data']['timelines'][0]['intervals'], list):
        print('intervals field exists but is not a list in response json!')
        return False
    if not len(responseContent['data']['timelines'][0]['intervals']) > 0:
        print('intervals field exists but is not a list in response json!')
        return False

    # values
    if not 'values' in responseContent['data']['timelines'][0]['intervals'][0]:
        return False

    # Structure looks ok, check for weather data fields
    if not 'temperature' in responseContent['data']['timelines'][0]['intervals'][0]['values']:
        return False
    if not 'weatherCode' in responseContent['data']['timelines'][0]['intervals'][0]['values']:
        return False
    if not 'windSpeed' in responseContent['data']['timelines'][0]['intervals'][0]['values']:
        return False
    if not 'windDirection' in responseContent['data']['timelines'][0]['intervals'][0]['values']:
        return False

    # All checks passed, structure is OK
    return True


def validate_temperature(temperature):
    if not type(temperature) == int and not type(temperature) == float:
        print('Temperature not a number!')
        return False
    if temperature > 80 or temperature < -50:
        print('Temperature outside range!')
        return False
    return True


def validate_weatherCode(weatherCode):
    if not type(weatherCode) == int:
        print('Weather code is not a number!')
        return False
    if not weatherCode in [4201, 4001, 4200, 6201, 6001, 6200, 6000, 4000, 7101, 7000, 7102, 5101, 5000, 5100, 5001, 8000, 2100, 2000, 1001, 1102, 1101, 1100, 1000]:
        print('Unknown weather code!')
        return False
    return True


def validate_windSpeed(windSpeed):
    if not type(windSpeed) == int and not type(windSpeed) == float:
        print('Wind speed not a number!')
        return False
    if windSpeed > 150 or windSpeed < 0:
        print('Wind speed outside range or negative!')
        return False
    return True


def validate_windDirection(windDirection):
    if not type(windDirection) == int and not type(windDirection) == float:
        print('Wind direction not a number!')
        return False
    if windDirection < 0 or windDirection > 360:
        print('Wind direction outside range!')
        return False
    return True


def retrieve_weather_data(config):
    # Data retrieving
    payload = {'location': str(config['latitude']) + ', ' + str(config['longitude']),
               'fields': 'temperature,weatherCode,windSpeed,windDirection',
               'timesteps': 'current',
               'units': 'metric',
               'apikey': config['apiKey'],
               }

    r = requests.get('https://api.tomorrow.io/v4/timelines', params=payload)

    # Log messages in cron will be sent by mail to the server user 'chocianowice'
    if r.status_code != 200:
        print('tomorrow.io weather API server did not return 200! Weather data retrieval aborted.')
        exit(1)

    responseContent = json.loads(r.content)

    if not check_response_body(responseContent):
        print('Malformed tomorrow.io API response!')
        exit(1)

    # Structure ok, so read values
    temperature = responseContent['data']['timelines'][0]['intervals'][0]['values']['temperature']
    weatherCode = responseContent['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
    windSpeed = responseContent['data']['timelines'][0]['intervals'][0]['values']['windSpeed']
    windDirection = responseContent['data']['timelines'][0]['intervals'][0]['values']['windDirection']

    return temperature, weatherCode, windSpeed, windDirection
