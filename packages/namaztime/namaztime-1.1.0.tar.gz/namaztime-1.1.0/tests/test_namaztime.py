import pytest
from namaztime import NamazTime

def test_namaz_time_today():
    namaz = NamazTime(city="Tashkent")
    result = namaz.today()
    assert isinstance(result, dict) or result == "You entered the wrong City!"
    if isinstance(result, dict):
        assert "Fajr" in result
        assert "Dhuhr" in result

def test_namaz_time_weekly():
    namaz = NamazTime(city="Tashkent")
    result = namaz.weekly()
    assert isinstance(result, dict)
    assert len(result) <= 7
    