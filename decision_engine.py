# -*- coding: utf-8 -*-
"""
@author: Kevin Sheng
"""

import json
from math import inf
from typing import Dict, Any, Optional
import itertools

class DecisionEngine:
    def __init__(self, table_path: str = "decision_table.json"):
        self.table_path = table_path
        # default bins boundaries, json bins will overide these
        self.bins = {
            "wind_speed_mps": [(0, 3), (3, 8), (8, inf)],
            "dry_bulb_temperature": [(-50, 5), (5, 25), (25, inf)],
            "precipitation_mm": [(0, 0.1), (0.1, 5), (5, inf)],
            "relative_humidity_pct": [(0, 30), (30, 60), (60, inf)],
        }
        self.mapping = {}
        self._load_table()

    def _load_table(self):
        # load decision table JSON into memory
        with open(self.table_path, "r", encoding="utf-8") as f:
            tbl = json.load(f)
        if "bins" in tbl:
            self.bins = self._coerce_bins(tbl["bins"])
        if "mapping" in tbl:
            self.mapping = tbl["mapping"]
        elif "rule" in tbl:
            print("[Info] Auto-generating mapping from rule ...")
            self.mapping = self._generate_mapping(tbl["rule"])
        else:
            raise ValueError("JSON must contain either 'mapping' or 'rule'.")
            
    def _generate_mapping(self, rule_expr: str):
        # auto-generate mapping for all 81 combinations (3^4)
        mapping = {}
        for combo in itertools.product([0, 1, 2], repeat=4):  # 81 combinations
            i1, i2, i3, i4 = combo
            s = i1 + i2 + i3 + i4
    
            if s <= 2:
                y = "A"
            elif s <= 5:
                y = "B"
            else:
                y = "C"
    
            mapping["".join(map(str, combo))] = y
        return mapping


    def _coerce_bins(self, b):
        # convert 'inf' strings to python inf in json file
        out = {}
        for k, ranges in b.items():
            fixed = []
            for lo, hi in ranges:
                lo = -inf if lo == "-inf" else (inf if lo == "inf" else lo)
                hi = inf if hi == "inf" else (-inf if hi == "-inf" else hi)
                fixed.append((float(lo), float(hi)))
            out[k] = fixed
        return out

    def _bin_index(self, val: Optional[float], bounds):
        # map nums to bin index
        if val is None:
            return 1
        for i, (lo, hi) in enumerate(bounds):
            if lo <= val < hi:
                return i
        return len(bounds) - 1

    def _key_from_payload(self, payload: Dict[str, Any]) -> str:
        # build codes
        wind = payload.get("wind_vector") or {}
        w = self._bin_index(wind.get("speed_mps"), self.bins["wind_speed_mps"])
        t = self._bin_index(payload.get("dry_bulb_temperature"), self.bins["dry_bulb_temperature"])
        p_raw = payload.get("precipitation_mm")
        p = self._bin_index(0.0 if p_raw is None else p_raw, self.bins["precipitation_mm"])
        h = self._bin_index(payload.get("relative_humidity_pct"), self.bins["relative_humidity_pct"])
        return f"{w}{t}{p}{h}"

    def decide(self, payload: Dict[str, Any]) -> str:
        # return final decision
        key = self._key_from_payload(payload)
        return self.mapping.get(key, "B")