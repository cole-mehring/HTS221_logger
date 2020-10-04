# Python script to find current
# weather details of any city
# using openweathermap api

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[val]

def get_weather():
    import requests, json
    import pytemperature
    # Enter your API key here
    open_weather_api_key = "2b8247bdc1ee06ed27fbc6c20d43a209"
    
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name
    city_name = 'Fargo'
    
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + open_weather_api_key + "&q=" + city_name
    
    # get method of requests module
    # return response object
    response = requests.get(complete_url)
    
    # json method of response object
    # convert json format data into
    # python format data
    website_response = response.json()
    
    # Now website_response contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if website_response["cod"] != "404":
        
        # Primary Fields
        main_formatted = website_response["main"]
        wind_formatted = website_response["wind"]
        weather_formatted = website_response["weather"]

        # Get the informatino
        kelvin_temperature = main_formatted["temp"]
        current_temperature = pytemperature.k2f(kelvin_temperature)
        current_humidity = main_formatted["humidity"]
        current_windspeed = wind_formatted["speed"]
        current_wind_direction = degToCompass(wind_formatted["deg"])
        current_wind_gusts = wind_formatted["gust"]
        current_weather = weather_formatted[0]["description"] # zeroeth index has description
        current_pressure = main_formatted["pressure"]

        return current_temperature, current_humidity, current_windspeed, current_wind_gusts, current_wind_direction, current_weather, current_pressure
    else:
        # Some sort of error occurred. Return errors.
        return "Error!", "Error!", "Error!", "Error!", "Error!", "Error!", "Error!"

