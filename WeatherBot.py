import requests
import telebot
from os import environ


def getWeatherFromCity(city: str, api_token: str):
    s_city = f"{city},RU"
    city_id = 0
    prognoz = ""
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           {'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': api_token})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (weather):", e)
        return f"Не удалось получить погоду по {city}\n ошибка {e}"
        pass

    # try:
    #     res = requests.get("http://api.openweathermap.org/data/2.5/weather",
    #                        {'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': api_token})
    #     data = res.json()
    #     # print("conditions:", data['weather'][0]['description'])
    #     # print("temp:", data['main']['temp'])
    #     # print("temp_min:", data['main']['temp_min'])
    #     # print("temp_max:", data['main']['temp_max'])
    #     conditions = data['weather'][0]['description']
    #     temp = data['main']['temp']
    #     temp_min = data['main']['temp_min']
    #     temp_max = data['main']['temp_max']
    #     # return f"Погодные условия: {conditions}\nСредняя температура на день: {temp}\nМинимальная температура на день: {temp_min}\nМаксимальная темпрература на день: {temp_max}"
    #
    # except Exception as e:
    #     print("Exception (weather):", e)
    #     return f"Не удалось получить погоду по {city}\n ошибка {e}"
    #     pass

    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           {'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': api_token})
        data = res.json()
        main = ""
        weatherDescription = ""
        dt_txt = ""
        number = 0
        for i in data['list']:
            if number == 17:
                break
            dt_txt = i['dt_txt']
            main = '{0:+3.0f}'.format(i['main']['temp'])
            weatherDescription = i['weather'][0]['description']
            prognoz = prognoz + f"{dt_txt} {main} {weatherDescription}\n"
            number = number + 1
        print(prognoz)
        print(number)
    except Exception as e:
        return f"Не удалось получить погоду по {city}\n ошибка {e}"
        pass
    return f"{prognoz}\n\n"

def main():
    api_telegram = environ.get("TELEGRAM_API_KEY")
    api_weather1 = environ.get("WEATHER_API_KEY")
    chat_id = environ.get("CHAT_ID2")
    bot = telebot.TeleBot(api_telegram)
    weather_in_novomoskovsk = getWeatherFromCity("Novomoskovsk", api_weather1)
    weather_in_gagarin = getWeatherFromCity("Gagarin", api_weather1)
    bot.send_message(
        chat_id,
        f"ЙОУ от Сереги. Че по погоде?\n\nНовомосковск\n\n{weather_in_novomoskovsk}Гагарин\n\n{weather_in_gagarin}"
    )


if __name__ == "__main__":
    main()
