import requests

def get_weather_data(city_name, api_key):
    # Busca coordenadas da cidade
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)

    if geo_response.status_code == 200 and geo_response.json():
        geo_data = geo_response.json()[0]
        lat = geo_data['lat']
        lon = geo_data['lon']

        # Busca clima atual usando lat e lon
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            return weather_response.json()

    return None

def get_forecast_data(city_name, api_key):
    # Obtem latitude e longitude
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)

    if geo_response.status_code == 200 and geo_response.json():
        geo_data = geo_response.json()[0]
        lat = geo_data['lat']
        lon = geo_data['lon']

        # Previsão para os próximos 5 dias
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            return forecast_response.json()

    return None
