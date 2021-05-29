# Description
Simple python script to retrieve data from tomorrow.io and store it into a mariadb database.

# Installation and usage
First of all you need an tomorrow.io API key. Go to [tomorrow.io](https://tomorrow.io) and create an account, so you will be able to get an API key.
Please keep your tomorrow.io subscription limits in mind when using as a cron job.

After you've received the key, copy the `config_template.yml` file and rename it to `config.yml`. Put all required data inside and save the new file.

To start the application simply call `python3 weather.py`.

# License
See LICENSE.md in the root directory.
