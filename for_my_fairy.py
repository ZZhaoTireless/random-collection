import json
import itchat
import schedule
import time
import datetime
from urllib.request import urlopen

itchat.auto_login(enableCmdQR=2)

def json_to_string(weather, city):
  return u"当前城市: {} \n当前温度: {}摄氏度 \n湿度: {} \n风力: {}级 \n描述: {}".format(city, weather["main"]["temp"], weather["main"]["humidity"], weather["wind"]["speed"], weather["weather"][0]["description"])

def forecast_to_string(forecast):
  min_temp = 1024
  max_temp = -1024
  rain = []
  for weather in forecast:
    if weather["main"]["temp_min"] < min_temp:
      min_temp = weather["main"]["temp_min"]
    if weather["main"]["temp_max"] > max_temp:
      max_temp = weather["main"]["temp_max"]
    if "3h" in weather["rain"]:
      date =  datetime.datetime.strptime(weather["dt_txt"], '%Y-%m-%d %H:%M:%S')
      hour = date.hour
      rain.append(u"{}点-{}点: 降雨量 {:5.2f}mm".format(hour + 5, hour + 8, weather["rain"]["3h"]))
  if len(rain) == 0:
    return u"未来12小时:\n最高气温: {}摄氏度 \n最低气温: {}摄氏度 \n无降雨".format(max_temp, min_temp)
  else:
    return u"未来12小时:\n最高气温: {}摄氏度 \n最低气温: {}摄氏度 \n可能降雨(mm: 毫米):\n{}".format(max_temp, min_temp, "\n".join(rain))

def job():
  # Here must setup an account on openweathermap.org to get private appid
  # The id here is the city id from openweathermap.org, you could search another city ids on its website
  # Here the 6176823 is waterloo
  waterloo_url = "http://api.openweathermap.org/data/2.5/weather?id=6176823&appid=*消音*&units=metric&lang=zh_cn"

  waterloo = json.load(urlopen(waterloo_url))
  
  # Here must setup an account on openweathermap.org to get private appid
  # The id here is the city id from openweathermap.org, you could search another city ids on its website
  # Here the 1796236 is ShangHai
  shanghai_url = "http://api.openweathermap.org/data/2.5/weather?id=1796236&appid=*消音*&units=metric&lang=zh_cn"

  shanghai = json.load(urlopen(shanghai_url))

  weather_waterloo = json_to_string(waterloo, u'滑铁卢')
  weather_shanghai = json_to_string(shanghai, u'上海')
  
  # Here must setup an account on openweathermap.org to get private appid
  # The id here is the city id from openweathermap.org, you could search another city ids on its website
  # The interval is 3 hours each so cnt = 4 will be the weather stats for the next 12 hours
  shanghai_forecast_url = "http://api.openweathermap.org/data/2.5/forecast?id=1796236&appid=*消音*&units=metric&lang=zh_cn&cnt=4"

  shanghai_forecast = json.load(urlopen(shanghai_forecast_url))
  forecast_shanghai = forecast_to_string(shanghai_forecast["list"])

  # Here must setup an unique alias for the friend who you will sent to
  dear = itchat.search_friends(name='*消音*')
  dear_username = dear[0]['UserName']

  itchat.send(u"这里是*消音*天气广播\n\n以下是当前的天气情况:\n\n{}\n{}\n\n{}".format(weather_shanghai, forecast_shanghai, weather_waterloo), toUserName=dear_username)

def init():
  # Here must setup an unique alias for the friend who you will sent to
  dear = itchat.search_friends(name='*消音*')
  dear_username = dear[0]['UserName']

  itchat.send(u"*消音*天气广播已经为宇宙第一可爱美丽善良的*消音*启动!\n每日更新时间为北京时间上午八点和晚上八点.\n希望*消音*开心.\n--机器人*消音*", toUserName=dear_username)

init()

schedule.every().day.at("08:00").do(job)
schedule.every().day.at("20:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

