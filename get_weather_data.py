# -*- coding: utf-8 -*-
"""
@author: Kevin Sheng
"""

import json
from typing import Dict, Any


class WeatherData:

    def __init__(self, json_file: str):
        self.json_file = json_file

    def _load(self) -> Dict[str, Any]:
        with open(self.json_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def extract(self) -> Dict[str, Any]:

        data = self._load()

        cur = (
            (data.get("weather", {}) or {})
            .get("interpreted_data", {})
            .get("area_summary", {})
            .get("current_conditions", {})
        )

        return {
            "wind_vector": {
                "speed_mps": cur.get("wind_speed_mps"),
                "direction_deg": cur.get("wind_direction_deg"),
            },
            "dry_bulb_temperature": cur.get("temperature_celsius"),
            "precipitation_mm": cur.get("precipitation_mm"),
            "relative_humidity_pct": cur.get("humidity_percent"),
        }


def main(json_file: str) -> Dict[str, Any]:
    return WeatherData(json_file).extract()


if __name__ == "__main__":
    result = main("data/response.json")
