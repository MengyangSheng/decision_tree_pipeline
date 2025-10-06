# -*- coding: utf-8 -*-
"""
@author: Kevin Sheng
"""

from decision_engine import DecisionEngine
from get_weather_data import WeatherData

wd = WeatherData("data/response.json")

payload = wd.extract()

payload["precipitation_mm"] = 0.0 if payload["precipitation_mm"] is None else payload["precipitation_mm"]

"""AUTO_REGENERATE toggle: True to rebuild decision_table.json automatically"""
AUTO_REGENERATE = True

if AUTO_REGENERATE:
    """regenerate decision_table.json from decision_tree.json"""
    print("[INFO] Regenerating decision table from decision_tree.json ...")
    engine = DecisionEngine("decision_tree.json")
    engine.export_table("decision_table.json")

else:
    """use existing keys in decison_table.json to decide"""
    print("[INFO] Using existing decision_table.json for decision ...")
    engine = DecisionEngine("decision_table.json")

decision = engine.decide(payload)
print("Decision =", decision)