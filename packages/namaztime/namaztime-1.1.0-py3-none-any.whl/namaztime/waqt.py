import os

import requests

import json
import datetime


class NamazTime:
    """
    Methods:
        today(): Returns prayer times for the current day.
        weekly(): Returns prayer times for the next 7 days.
        get_special_date(date): Returns prayer times for a specific date.
    """
    def __init__(self, city, school=1, timezone="UTC", method=3):
        """
        NamazTime class provides functionalities to retrieve Islamic prayer times
        for a given city. It fetches prayer timings from the Aladhan API and supports
        daily and weekly schedules.

        Args:
            city (str): The city name for which prayer times are needed.
            school (int, optional): The fiqh school (0 for Shafi'i, 1 for Hanafi). Default is 1
            timezone (str, optional): The timezone of the city. Default is "UTC"
            method (int, optional): The calculation method for prayer times. Default is 3(Muslim World League)
        """
        self.city = city
        self.school = school
        self.timezone = timezone
        self.method = method


    def today(self):
        """
        Fetches prayer times for the current date.

        Returns:
            dict: A dictionary containing prayer times and related information.
            str: An error message if the city name is incorrect or data retrieval fails.
        """
        today = datetime.date.today().strftime("%d-%m-%Y")
        try:
            return self.__get_namaz_time(today)
        except:
            return "You entered the wrong City!"


    def weekly(self):
        """
        Fetches prayer times for the next 7 days, starting from today.

        Returns:
            dict: A dictionary where keys are dates (formatted as "dd-mm-yyyy"),
                  and values contain the prayer timings for each day.
        """
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=6)
        start_str = start_date.strftime("%d-%m-%Y")
        end_str = end_date.strftime("%d-%m-%Y")


        set_timezone = self.__set_timezone()
        url = (
            f"https://api.aladhan.com/v1/calendarByAddress?address={self.city}"
            f"&method={self.method}&school={self.school}&timezonestring={self.timezone}"
            f"&start={start_str}&end={end_str}"
        )

        response = requests.get(url)
        try:
            data = response.json()
        except ValueError:
            return "❌ Error: No response in JSON format"

        weekly_times = {}
        for day in data["data"]:
            date = day["date"]["gregorian"]["date"]
            date_obj = datetime.datetime.strptime(date, "%d-%m-%Y").date()

            if start_date <= date_obj <= end_date:
                weekly_times[date] = self.__calculate_namaz_periods(day, day["timings"])

        return weekly_times


    def __set_timezone(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(BASE_DIR, "timezone_city.json")

        with open(json_path, "r", encoding="utf-8") as file:
            timezones = json.load(file)

        for timezone in timezones.get("timezones"):
            if self.city.lower() in timezone.lower():
                self.timezone = timezone
                return timezone
        return 'UTC'

    def get_special_date(self, date):
        """
        Retrieves prayer times for a specific date.

        Args:
            date (str): The date in "dd-mm-yyyy" format.

        Returns:
            dict: Prayer times and related information.
        """
        return self.__get_namaz_time(date)


    def __get_namaz_time(self, date):
        self.__set_timezone()
        url = (
            f"https://api.aladhan.com/v1/timingsByAddress/{date}"
            f"?address={self.city}&method={self.method}&shafaq=general"
            f"&tune=5,3,5,7,9,-1,0,8,-6&school={self.school}"
            f"&timezonestring={self.timezone}&calendarMethod=UAQ"
        )

        response = requests.get(url)
        try:
            data = response.json()
        except ValueError:
            return "❌ Error: No response in JSON format"

        timings = data["data"].get("timings")
        return self.__calculate_namaz_periods(data["data"], timings)


    def __calculate_namaz_periods(self, data, timings):
        periods = {
            "Fajr": timings["Fajr"],
            "Sunrise": timings["Sunrise"],
            "Dhuhr": timings["Dhuhr"],
            "Asr": timings["Asr"],
            "Maghrib": timings["Maghrib"],
            "Isha": timings["Isha"],
            "Gregorian Date": data["date"]["gregorian"]["date"],
            "Hijri Date": data["date"]["hijri"]["date"],
            "Hijri Month": data["date"]["hijri"]["month"]["en"],
            "Weekday": data["date"]["gregorian"]["weekday"]["en"],
            "Timezone": data["meta"]["timezone"],
            "Method": data["meta"]["method"]["name"],
            "school": data["meta"]["school"],
        }

        return periods
