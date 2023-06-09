from env_canada import ECWeather, ECRadar, ECAirQuality
from geopy import Nominatim
from io import BytesIO
from PIL import Image
from geopy.exc import GeocoderUnavailable, GeocoderServiceError, GeocoderTimedOut
import requests

try:
    from config import use_openweathermap_geocoding
    
    if use_openweathermap_geocoding == False:
        pass
    
    elif use_openweathermap_geocoding == True:
        from config import open_weathermap_api_key
        if open_weathermap_api_key == None or open_weathermap_api_key == "" or open_weathermap_api_key == "OPEN_WEATHERMAP_API_KEY_HERE":
            raise ImportError

except ImportError:
    print("openweathermap_api_key not found in config.py, either set use_openweathermap_geocoding to False or set openweathermap_api_key")


class get_weather:

    async def forecast(location):
        latitude,longitude = await get_weather.get_location(city=location)
        air_quality = ECAirQuality(coordinates=(latitude,longitude))
        weather = ECWeather(coordinates=(latitude,longitude))
        await air_quality.update()
        await weather.update()
        forecast = weather.daily_forecasts
        x=0
        weather_summaries = []
        weather_times = []
        for i in range(12):
            weather_summaries.append(forecast[x]['text_summary'])
            weather_times.append(forecast[x]['period'])
            x += 1
        return weather_times, weather_summaries, air_quality.current
        
    async def warnings(location):
        latitude, longitude = await get_weather.get_location(city=location)
        alerts = ECWeather(coordinates=(latitude,longitude))
        await alerts.update()
        warnings = alerts.alerts
        warning_text = []
        warning_time = []
        try:
            alert_title = warnings['warnings']['value'][0]['title']
            alert_time = warnings['warnings']['value'][0]['date']
            warning_text.append(alert_title)
            warning_time.append(alert_time)
        except IndexError:
            warning_text.append("No warnings")
            warning_time.append("No warnings")
        finally:
            try:
                watch_title = warnings['watches']['value'][0]['title']
                watch_time = warnings['watches']['value'][0]['date']
                warning_text.append(watch_title)
                warning_time.append(watch_time)
            except IndexError:
                warning_text.append("No watches")
                warning_time.append("No watches")
            finally:
                try:
                    advisory_title = warnings['advisories']['value'][0]['title']
                    advisory_time = warnings['advisories']['value'][0]['date']
                    warning_text.append(advisory_title)
                    warning_time.append(advisory_time)
                except IndexError:
                    warning_text.append("No advisories")
                    warning_time.append("No advisories")
                finally:
                    try:
                        statement_title = warnings['statements']['value'][0]['title']
                        statement_time = warnings['statements']['value'][0]['date']
                        warning_text.append(statement_title)
                        warning_time.append(statement_time)
                    except IndexError:
                        warning_text.append("No statements")
                        warning_time.append("No statements")

                    finally:
                        return warning_text, warning_time
        
            
    async def radar(location,image_format):

        latitude, longitude = await get_weather.get_location(city=location)
        radar = ECRadar(coordinates=(latitude, longitude))
    
        if image_format == 'png':
            radar_data = await radar.get_latest_frame()
            radar_image = Image.open(BytesIO(radar_data))
            assert radar_image.format == 'PNG'
            radar_image.save('radar.png')
            return radar_image
            
        elif image_format == 'gif':
            radar_data = await radar.get_loop(fps=5)
            radar_image = Image.open(BytesIO(radar_data))
            assert radar_image.format == 'GIF'
            radar_image.save('radar.gif', save_all=True)
            return radar_image

    async def air_quality(location):
        
        latitude,longitude = await get_weather.get_location(city=location)
        air_quality = ECAirQuality(coordinates=(latitude,longitude))
        await air_quality.update()  
        print(air_quality.current)

        if air_quality.current == None:
                raise AirQualityNotFoundError

        else:
            return air_quality.current
            
    async def get_location(city):
        try:
            locator = Nominatim(user_agent="ForecastFriend")
            location = locator.geocode(city, country_codes='ca')
            return location.latitude, location.longitude
        
        except GeocoderUnavailable or GeocoderServiceError or GeocoderTimedOut:
            if use_openweathermap_geocoding == True:
                print("GeocoderUnavailable, using OpenWeatherMap API")
                try:
                    parameters = {
                        "q": f"{city},CA",
                        "limit": "1",
                        "appid": open_weathermap_api_key
                    }
                    location = requests.get("https://api.openweathermap.org/geo/1.0/direct", params=parameters)
                    data = location.json()
                    latitude = data[0]['lat']
                    longitude = data[0]['lon']
                    return latitude, longitude
                
                except IndexError:
                    raise LocationNotFoundError
                
                except requests.exceptions.HTTPError:
                    raise LocationNotFoundError
                
                except KeyError:
                    raise LocationNotFoundError
                
            elif use_openweathermap_geocoding == False:
                raise LocationNotFoundError

        except AttributeError:
            raise LocationNotFoundError

class LocationNotFoundError(Exception):
    pass

class WarningNotFoundError(Exception):
    pass

class AirQualityNotFoundError(Exception):
    pass
