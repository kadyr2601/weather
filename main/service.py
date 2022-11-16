import time
from bs4 import BeautifulSoup
from selenium import webdriver
from main.models import Weather
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# def driver():
#     # driver = webdriver.Remote('http://172.21.0.3:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
#     driver = webdriver.Chrome(executable_path="/home/kadyr/Desktop/weather/driver/chromedriver",
#                               desired_capabilities=DesiredCapabilities.CHROME)
#     driver.get("https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/")
#     return driver


def add_weather(date, temp, desc) -> None:
    if Weather.objects.filter(date=date).exists():
        obj = Weather.objects.get(date=date)
        obj.temperature = temp
        obj.weather_description = desc
        obj.save()
    else:
        Weather.objects.create(date=date, temperature=temp, weather_description=desc)


def get_today_info():
    driver = webdriver.Remote('http://172.21.0.2:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    # driver = webdriver.Chrome(executable_path="/app/backend/driver/chromedriver",
    #                           desired_capabilities=DesiredCapabilities.CHROME)
    driver.get("https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/")
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # get today
        today = soup.find("div", {"class": "city__day fl-col active"})
        # get today temperature
        temp = soup.find("div", {"class": "city__main-temp"})
        # get today description
        desc = soup.find("span", {"class": "city__main-image-descr"}).find_all("span")

        if len(desc) > 1:
            add_weather(today.get("id"), temp.text, f"{desc[0].text} {desc[1].text}")
            return {
                "date": today.get('id'), "temperature": temp.text, "weather_description": f"{desc[0].text} {desc[1].text}"
            }
        else:
            add_weather(today.get("id"), temp.text, desc[0].text)
            return {"date": today.get('id'), "temperature": temp.text, "weather_description": desc[0].text}
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def get_day_info(id):
    driver = webdriver.Remote('http://172.21.0.2:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    # driver = webdriver.Chrome(executable_path="/app/backend/driver/chromedriver",
    #                           desired_capabilities=DesiredCapabilities.CHROME)
    driver.get("https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/")
    try:
        driver.find_element("id", id).click()
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(2)
        # get day
        day = soup.find("div", {"class": "city__main active"})
        # get today temperature
        temp = soup.find("div", {"class": "city__main-temp"})
        # get day description
        desc = soup.find("span", {"class": "city__main-image-descr"}).find_all("span")

        if len(desc) > 1:
            add_weather(day.get("data-id"), temp.text, f"{desc[0].text} {desc[1].text}")
            return {
                "date": day.get('data-id'), "temperature": temp.text, "weather_description": f"{desc[0].text} {desc[1].text}"
            }
        else:
            add_weather(day.get("data-id"), temp.text, desc[0].text)
            return {"date": day.get('data-id'), "temperature": temp.text, "weather_description": desc[0].text}
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def parser():
    driver = webdriver.Remote('http://172.21.0.2:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    # driver = webdriver.Chrome(executable_path="/app/backend/driver/chromedriver",
    #                           desired_capabilities=DesiredCapabilities.CHROME)
    driver.get("https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/")
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result = []
        data = get_today_info()
        result.append(data)
        five_days = soup.find_all("div", {"class": "city__day fl-col"})
        for i in five_days:
            data = get_day_info(i.get('id'))
            result.append(data)
        return result
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
