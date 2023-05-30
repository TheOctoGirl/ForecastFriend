# ForecastFriend
![Python 3.10](https://img.shields.io/badge/Python-3.10-informational)

Forecast Friend is a discord bot that allows you to get weather data from Environment Canada right in Discord. Forecast Friend is written in Python and is based on [env_canada](https://github.com/michaeldavie/env_canada) and [nextcord](https://github.com/nextcord/nextcord).

# Features
- Get forecast data from Environment Canada
- Get the current radar imagery from Environment Canada
- Get the current weather warnings from Environment Canada
- Get the current air quality data from Environment Canada
- Ability to input a location by city name

# Installation

## Invite Link
To get Forecast Friend on your server, use this [invite link](https://discord.com/api/oauth2/authorize?client_id=1062573146630262784&permissions=0&scope=bot).

## Self Hosting

### Pre-requisites
- Python 3.10 or higher
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Stable Version
#### Installation
1. Get the latest release from the [releases page](https://github.com/TheOctoGirl/ForecastFriend/releases/latest)
2. Extract the zip file
3. Change directory into the extracted directory
4. Install the required packages using `pip install -r requirements.txt`
5. Rename `default_config.py` to `config.py`
6. Edit `config.py` and add your Discord bot token
7. Run `python3 main.py`


### Beta Version
#### Installation
1. Clone the repository
2. Change directory into the cloned repository directory
3. Install the required packages using `pip install -r requirements.txt`
4. Rename `default_config.py` to `config.py`
5. Edit `config.py` and add your Discord bot token
6. Run `python3 main.py`

# Bugs and Feature Requests
If you find a bug or have a feature request, please open an [issue](https://github.com/TheOctoGirl/ForecastFriend/issues).

# Screenshots
<img width="1008" alt="Forecast Friend forecast command" src="https://user-images.githubusercontent.com/119755793/235819221-97c41289-f631-4688-a9e5-b398b75ac21c.png">
<img width="260" alt="Forecast Friend air quality command" src="https://user-images.githubusercontent.com/119755793/235819288-2b125d1b-43c4-4ecb-928d-e1f84f88abbb.png">
<img alt="Forecast Friend radar command" src="https://user-images.githubusercontent.com/119755793/235819331-64491aef-01c2-4fcb-b3b4-5e1b8bf8d52f.gif">

