# main.py
DEBUG_WITHOUT_EINK = True

if not DEBUG_WITHOUT_EINK:
    import eink
import weather
import chart
from PIL import Image
import logging
import sys
import os

tmpdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp_image')

# program is run on crontab -e
# 0 0 * * * /usr/bin/python3 /home/pi/PycharmProjects/weather/main.py

if __name__ == '__main__':
    city = ["vancouver,ca"]

    logging.info("get weather for city")
    # city_latlog = weather.get_latlon_data(["cambridge"])
    weather_data = weather.get_weather_data(city, imperial=False)

    # pp(weather_data)
    """
    query_url = weather.build_weather_query(city, imperial)
    print(query_url)
    weather_data = weather.get_api_data(query_url)
    pp(weather_data)
    weather.display_weather_info(weather_data, imperial)
    """

    chart.plot_temperature_precipitation(weather_data)
    chart.show_current_weather(weather_data)
    chart.show_week(weather_data)
    chart.show_alert(weather_data)
    chart.show_date(city_label="Vancouver, Canada")
    chart.combine_for_display()

    # eink.clear()
    if not DEBUG_WITHOUT_EINK:
        eink.show(eink.convert_color(tmpdir + '/weather_combined.png'))
