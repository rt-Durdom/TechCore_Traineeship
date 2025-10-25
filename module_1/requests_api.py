from requests import get


def weather_openapi(lat=55.7558, lon=37.6173, days=3):
    """Получить прогноз погоды"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days={days}"

    data = (get(url)).json()

    print(f"Прогноз на {days} дней:")
    for i in range(days):
        date = data['daily']['time'][i]
        temp_max = data['daily']['temperature_2m_max'][i]
        temp_min = data['daily']['temperature_2m_min'][i]
        precip = data['daily']['precipitation_sum'][i]

        print(f"{date}: {temp_min}°C - {temp_max}°C, осадки: {precip}mm")


if __name__ == '__main__':
    weather_openapi()
