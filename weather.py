import yaml
import retriever
import exporter
import os


# This code only loads the config and triggers the respective functions that do all the work

root_dir = os.path.abspath(os.path.dirname(__file__))
config = yaml.safe_load(open(root_dir + "/config.yml"))


temperature, weatherCode, windSpeed, windDirection = retriever.retrieve_weather_data(
    config['tomorrow_io'])


exporter.export_to_db(config['database'],
                      temperature,
                      weatherCode,
                      windSpeed,
                      windDirection)
