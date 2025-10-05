# -*- coding: utf-8 -*-
"""
@author: Kevin Sheng
"""

from decision_engine import DecisionEngine
from get_weather_data import WeatherData

wd = WeatherData("data/response.json")

payload = wd.extract()

payload["precipitation_mm"] = 0.0 if payload["precipitation_mm"] is None else payload["precipitation_mm"]


"""we can choose whether to use keys in decison_table.json or generate keys using decision_tree.json"""
#engine = DecisionEngine("decision_table.json")
engine = DecisionEngine("decision_tree.json")

"""save the generated keys to decision_table.json"""
engine.export_table("decision_table.json")

print("decision =", engine.decide(payload))