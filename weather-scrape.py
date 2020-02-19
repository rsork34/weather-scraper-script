import requests
import sys
from bs4 import BeautifulSoup

ERROR_MESSAGE = 'Error: requires command line argument for "hour", today" or "week"'

# Ensure only program name and command are entered
if len(sys.argv) != 2:
    print(ERROR_MESSAGE)
    exit()

# Ensure that command is valid
command = sys.argv[1]
if command != 'hour' and command != 'today' and command != 'week':
    print(ERROR_MESSAGE)
    exit()

if command == 'hour':
    timeInfo = 'Weather this hour: '
    CURRENT_URL = 'https://weather.com/en-CA/weather/hourbyhour/l/62e0efebee1ac0e8fa9b21fd17d57a6a0001753ab6be8a4874bb78bbb52eda02'
elif command == 'today':
    CURRENT_URL = 'https://weather.com/en-CA/weather/today/l/62e0efebee1ac0e8fa9b21fd17d57a6a0001753ab6be8a4874bb78bbb52eda02'
    timeInfo = 'Weather today: '
elif command == 'week':
    CURRENT_URL = 'https://weather.com/en-CA/weather/5day/l/62e0efebee1ac0e8fa9b21fd17d57a6a0001753ab6be8a4874bb78bbb52eda02'
    timeInfo = 'Weather this week: '

# Get and parse page depending on command
page = requests.get(CURRENT_URL)
soup = BeautifulSoup(page.content, 'lxml')

# Find and print weather for current hour
if command == 'hour':
    weather = soup.find('td', {'class' : 'temp'}).span.text
    print(timeInfo + weather)

# Find and print todays weather
elif command == 'today':
    weather = soup.find('div', {'class' : 'today_nowcard-temp'}).span.text
    print(timeInfo + weather)

# Find and print high/low weather for next 5 days
elif command == 'week':
    # Array of each day weather is printed for
    days = soup.findAll('span', {'class' : 'date-time'})
    for i, day in enumerate(days):
        days[i] = day.text

    # Get list of high/low weather for each day of the week
    dailyWeatherList = soup.findAll('td', {'class' : 'temp'})
    dailyWeather = []
    for day in dailyWeatherList:
        dailyWeather.extend(day.findAll('span'))
    
    # Remove emptry strings from list
    for day in dailyWeather:
        if day.text == '':
            dailyWeather.remove(day)

    # Print weather for each day including high/low temp
    # Formatted:
    #           Day: High: X, Low: Y
    j = 0 # Keeps track of high/low for current day
    for i, day in enumerate(days):
        curString = day + ': High: ' + dailyWeather[j].text + ', Low: ' + dailyWeather[j + 1].text
        j += 2
        print(curString)



