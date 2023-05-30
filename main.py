import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import weather_api
from weather_api import LocationNotFoundError, WarningNotFoundError, AirQualityNotFoundError


intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    game = nextcord.Activity(name='for /weather', type=3)
    await bot.change_presence(status=nextcord.Status.online,activity=game)
    print(f'We have logged on as {bot.user}')

@bot.slash_command()
async def weather(interaction:nextcord.Interaction):
    pass


@weather.subcommand(description='Get the weather from Environment Canada')
async def forecast(interaction: nextcord.Interaction, city: str = SlashOption(description='The city you would like the weather for', required=True)):
    try:
        await interaction.response.defer(ephemeral=True)
        weather_times, weather_summaries, air_quality = await weather_api.get_weather.forecast(city)
        await interaction.send(f'Time: {weather_times[0]}\nAir Quality: {air_quality}\nSummary: {weather_summaries[0]}\n\nTime: {weather_times[1]}\nSummary: {weather_summaries[1]}\n\nTime: {weather_times[2]}\nSummary: {weather_summaries[2]}\n\nTime: {weather_times[3]}\nSummary: {weather_summaries[3]}\n\nTime: {weather_times[4]}\nSummary: {weather_summaries[4]}\n\nTime: {weather_times[5]}\nSummary: {weather_summaries[5]}\n\nTime: {weather_times[6]}\nSummary: {weather_summaries[6]}\n\nTime: {weather_times[7]}\nSummary: {weather_summaries[7]}\n\nTime: {weather_times[8]}\nSummary: {weather_summaries[8]}\n\nTime: {weather_times[9]}\nSummary: {weather_summaries[9]}\n\nTime: {weather_times[10]}\nSummary: {weather_summaries[10]}\n\nTime: {weather_times[11]}\nSummary: {weather_summaries[11]}', ephemeral=True)
    
    except LocationNotFoundError:
        await interaction.send('The specified city is not found', ephemeral=True)
    

@weather.subcommand(description='Get weather warnings from Environment Canada')
async def warnings(interaction: nextcord.Interaction, city: str = SlashOption(description='The city you would like the weather alerts for', required=True)):
    try:
        weather_alert_title, weather_alert_time_issued = await weather_api.get_weather.warnings(city)
        await interaction.send(f'Warning: {weather_alert_title}\nTime Issued: {weather_alert_time_issued}', ephemeral=True)
    
    except WarningNotFoundError:
       await interaction.send('There are no weather alerts for the specified city')

    except:
        await interaction.send('An unknown error occurred')

@weather.subcommand(description='Get radar imagery from Environment Canada')
async def radar(interaction: nextcord.Interaction,city: str = SlashOption(description='The city you would like the radar for', required=True), image: str = SlashOption(description='Animated GIF or Static PNG', choices=['gif','png'],required=True)):
    await interaction.response.defer(ephemeral=True)
    try:
        await weather_api.get_weather.radar(city,image)
        await interaction.send(file=nextcord.File(f'radar.{image}'), ephemeral=True)
    
    except LocationNotFoundError:
        await interaction.send('The specified city is not found', ephemeral=True)

@weather.subcommand(description='Get the current air quality from Environment Canada')
async def air_quality(interaction: nextcord.Interaction, city: str = SlashOption(description='The city you would like the air quality for', required=True)):
    try:
        air_quality = await weather_api.get_weather.air_quality(city)
        await interaction.send(f'Air Quality: {air_quality}', ephemeral=True)
    
    except LocationNotFoundError:
        await interaction.send('The specified city is not found', ephemeral=True)

    except AirQualityNotFoundError:
        await interaction.send('There is no air quality data for the specified city', ephemeral=True)

if __name__ == '__main__':
    try:
        from config import discord_api_key
        bot.run(discord_api_key)
    except ImportError:
        print('config.py not set up. Please rename default_config.py to config.py and fill in the required fields')
        quit()
