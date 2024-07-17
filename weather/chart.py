# chart.py

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime
import calendar
import sys
import os

imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weather images')
tmpdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp_image')
# if os.path.exists(imgdir):
#    sys.path.append(imgdir)

def plot_temperature_precipitation(weather_data):
    """
    Plot temperature and precipitation in a graph
    :param weather_data: json of weather data
    :return:plt of data
    """

    # pp(weather_data)
    hourly_data = [weather_data["hourly"][:]][0]

    temp_data = [item["temp"] for item in hourly_data]
    pop_data = [item["pop"] for item in hourly_data]
    t = np.arange(0, 25)

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_ylabel('Precipitation', color=color)
    ax1.bar(t, pop_data[0:25], width=1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 1)

    plt.grid(axis='x')
    ax1.set_xticks(np.arange(0, 25, 6))
    ax1.set_xticks(np.arange(0, 25, 1), minor=True)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_xlabel('time (hr)')
    ax2.set_ylabel('temperature', color=color, )
    ax2.plot(t, temp_data[0:25], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    ax1.set_xlim(0, 24)
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax2.yaxis.tick_left()
    ax2.yaxis.set_label_position("left")

    fig.set_size_inches(4, 2)

    fig.tight_layout()
    plt.savefig(tmpdir + '/weather_chart.png')
    # plt.show()
    return Image.open(tmpdir + '/weather_chart.png')


def show_current_weather(weather_data):
    # img = cv2.imread('weather images/01.png', 1)
    # img_stretch = cv2.resize(img, (100, 100))
    # cv2.imshow('Resized Image', img_stretch)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    background = Image.new("RGBA", (400, 200))
    draw = ImageDraw.Draw(background)
    draw.rectangle(((0, 0), (400, 200)), fill="white", outline="white")
    icon_path = weather_data['daily'][0]['weather'][0]['icon']
    im = Image.open(imgdir+ '/' + icon_path[0:2] + '.png')
    im = im.resize((120, 120))
    background.paste(im, (20, 10), im)
    font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    font_large = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSans.ttf', 72)
    draw.fontmode = "1"
    draw.text((22, 135),
              weather_data['daily'][0]['weather'][0]['description'],
              fill="black", font=font, align="left")

    draw.text((200, 10),
              str(round(weather_data['daily'][0]['temp']['max'])) + "°C/\n" +
              str(round(weather_data['daily'][0]['temp']['min'])) + "°C",
              fill="orange", font=font_large, align="left")

    if weather_data['daily'][0]['wind_deg'] < 1 * 360 / 16:
        wind_direction = "N"
    elif weather_data['daily'][0]['wind_deg'] < 3 * 360 / 16:
        wind_direction = "NE"
    elif weather_data['daily'][0]['wind_deg'] < 5 * 360 / 16:
        wind_direction = "E"
    elif weather_data['daily'][0]['wind_deg'] < 7 * 360 / 16:
        wind_direction = "SE"
    elif weather_data['daily'][0]['wind_deg'] < 9 * 360 / 16:
        wind_direction = "S"
    elif weather_data['daily'][0]['wind_deg'] < 11 * 360 / 16:
        wind_direction = "SW"
    elif weather_data['daily'][0]['wind_deg'] < 13 * 360 / 16:
        wind_direction = "W"
    elif weather_data['daily'][0]['wind_deg'] < 15 * 360 / 16:
        wind_direction = "NW"
    else:
        wind_direction = "N"

    draw.text((10, 170),
              " PCPN: " + str(round(weather_data['daily'][0]['pop'])) + "mm ",
              fill="blue", font=font, align="left")
    draw.text((140, 170),
              " RH: " + str(round(weather_data['daily'][0]['humidity'])) + "% ",
              fill="blue", font=font, align="left")
    draw.text((240, 170),
              " WND: " + wind_direction + " " + str(round(weather_data['daily'][0]['wind_speed'])) + "m/s ",
              fill="green", font=font, align="left")

    #    draw.text((200, 100),
    #              " pop:         " + str(weather_data['daily'][0]['pop']) + "mm \n"
    #              " humidity:        " + str(weather_data['daily'][0]['humidity']) + "% \n"
    #              " wind:   " + wind_direction + " " + str(weather_data['daily'][0]['wind_speed']) + "m/s ",
    #              fill="red", font=font, align="left")

    # background.show()
    background.save(tmpdir + '/weather_icon.png')
    return background


def show_date(city_label=""):
    now = datetime.datetime.now()
    # print(now.strftime("%Y-%m-%d %H:%M:%S"))
    # print(calendar.day_name[now.today().weekday()])
    background = Image.new("RGBA", (400, 100))
    draw = ImageDraw.Draw(background)
    draw.rectangle(((0, 0), (400, 100)), fill="white")

    font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    font_large = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSans.ttf', 52)
    draw.fontmode = "1"

    draw.text((20, 10),
              city_label,
              fill="black", font=font, align="left")
    draw.text((20, 32),
              calendar.day_name[now.today().weekday()][0:3],
              fill="black", font=font_large, align="left")
    draw.text((246, 10),
              now.strftime("%H:%M"),
              fill="black", font=font, align="right")
    draw.text((325, 10),
              now.strftime("%Y-"),
              fill="black", font=font, align="right")
    draw.text((245, 32),
              now.strftime("%m-%d"),
              fill="black", font=font_large, align="right")

    background.save(tmpdir + '/date.png')
    return background


def show_week(weather_data):
    background = Image.new("RGBA", (400, 90))
    draw = ImageDraw.Draw(background)
    draw.rectangle(((0, 0), (400, 90)), fill="white", outline="white")

    for count in range(1, 8):
        icon_path = weather_data['daily'][count]['weather'][0]['icon']
        im = Image.open(imgdir+ '/' + icon_path[0:2] + '.png')
        im = im.resize((40, 40))
        background.paste(im, (count * 55 - 45, 25), im)

        font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 14)
        draw.fontmode = "1"
        draw.text((count * 55 - 45, 70),
                  str(round(weather_data['daily'][count]['temp']['day'])) + "ºC\n",
                  fill="orange", font=font, align="left")
        draw.text((count * 55 - 40, 5),
                  calendar.day_name[(datetime.datetime.now().today().weekday() + count) % 7][0:3],
                  fill="black", font=font, align="left")

    background.save(tmpdir + '/week.png')
    return background


def show_alert(weather_data):
    background = Image.new("RGBA", (400, 40))
    draw = ImageDraw.Draw(background)
    draw.rectangle(((0, 0), (400, 40)), fill="white", outline="white")

    font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    draw.fontmode = "1"
    if 'alerts' in weather_data:
        draw.text((10, 10),
                  weather_data['alerts'][0]['event'],
                  fill="red", font=font, align="left")
    else:
        draw.text((10, 10),
                  "no alerts",
                  fill="green", font=font, align="left")

    background.save(tmpdir + '/alerts.png')
    return background


def combine_for_display():
    im0 = Image.new("RGB", (400, 640))
    draw = ImageDraw.Draw(im0)
    draw.rectangle(((0, 0), (400, 640)), fill="yellow")

    im1 = Image.open(tmpdir + '/weather_icon.png')
    im2 = Image.open(tmpdir + '/weather_chart.png')
    im3 = Image.open(tmpdir + '/date.png')
    im4 = Image.open(tmpdir + '/week.png')
    im5 = Image.open(tmpdir + '/alerts.png')

    im0.paste(im1, (0, 102))
    im0.paste(im2, (0, 304))
    im0.paste(im3, (0, 0))
    im0.paste(im4, (0, 506))
    im0.paste(im5, (0, 598))
    im0.save(tmpdir + '/weather_combined.png')
    return im0


if __name__ == "__main__":
    # do something
    print("hi")
