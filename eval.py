# -*- coding: utf-8 -*-
"""
@author: Kevin Sheng
"""

from decision_engine import DecisionEngine
from get_weather_data import WeatherData

wd = WeatherData("data/response.json")

payload = wd.extract()

payload["precipitation_mm"] = 0.0 if payload["precipitation_mm"] is None else payload["precipitation_mm"]

engine = DecisionEngine("decision_table.json")

print("decision =", engine.decide(payload))