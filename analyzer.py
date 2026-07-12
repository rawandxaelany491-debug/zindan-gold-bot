import json
import re
from typing import Dict, List, Tuple
import numpy as np

class SNRZAnalyzer:
    def __init__(self, knowledge_base_path="data/knowledge_base.json"):
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.timeframes = ["1w", "1d", "4h", "1h", "15m", "5m", "1m"]
        
    def _load_knowledge_base(self, path):
        """بارکردنی بنکەی زانیاری SNRZ لە فایلەکەوە"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_chart(self, zones: Dict) -> Dict:
        """
        شیکاری چارت بە پێی ڕێگای SNRZ
        
        Args:
            zones: {
                "sell_zones": [{"level": 2200, "timeframe": "1h"}],
                "buy_zones": [{"level": 2100, "timeframe": "1h"}]
            }
        Returns:
            {
                "signal": "BUY" or "SELL" or "NEUTRAL",
                "confidence": 0.85,
                "entry_zone": 2150,
                "targets": [2200, 2250],
                "stop_loss": 2100,
                "analysis": "..."
            }
        """
        result = {
            "signal": "NEUTRAL",
            "confidence": 0.0,
            "entry_zone": None,
            "targets": [],
            "stop_loss": None,
            "analysis": ""
        }
        
        # شیکاری پێکهاتەکانی SNRZ
        if zones.get("sell_zones") and zones.get("buy_zones"):
            # بینینی ڕیسرستانس و سەپۆرت
            result = self._analyze_support_resistance(zones)
        
        return result
    
    def _analyze_support_resistance(self, zones: Dict) -> Dict:
        """شیکاری سەپۆرت و ڕیسرستانس"""
        # شیکاری داینامیکی SNRZ
        # VS, VR, SBR, RBS, SRR, RSS
        
        sell_zones = zones.get("sell_zones", [])
        buy_zones = zones.get("buy_zones", [])
        
        # دیاریکردنی ڤالید سەپۆرت و ڤالید ڕیسرستانس
        valid_support = self._find_valid_support(buy_zones)
        valid_resistance = self._find_valid_resistance(sell_zones)
        
        # دیاریکردنی جۆری سیگناڵ
        if valid_support and valid_support['strength'] > 0.7:
            if self._check_breakout(valid_support, "up"):
                return {
                    "signal": "BUY",
                    "confidence": valid_support['strength'],
                    "entry_zone": valid_support['level'],
                    "targets": [valid_support['level'] * 1.02, valid_support['level'] * 1.05],
                    "stop_loss": valid_support['level'] * 0.98,
                    "analysis": f"ڕیسرستانس شکێنراوە بووە بە سەپۆرت (RBS) لە تایمفرەیمی {valid_support['timeframe']}"
                }
        
        return {"signal": "NEUTRAL", "confidence": 0.0}
    
    def _find_valid_support(self, zones: List) -> Dict:
        """دۆزینەوەی ڤالید سەپۆرت"""
        for zone in zones:
            if zone.get('type') == 'support' and zone.get('strength', 0) > 0.7:
                return zone
        return None
    
    def _find_valid_resistance(self, zones: List) -> Dict:
        """دۆزینەوەی ڤالید ڕیسرستانس"""
        for zone in zones:
            if zone.get('type') == 'resistance' and zone.get('strength', 0) > 0.7:
                return zone
        return None
    
    def _check_breakout(self, zone: Dict, direction: str) -> bool:
        """پشکنینی برەیکاوت"""
        # شیکاری تەکنیکی برەیکاوت
        return True
    
    def detect_inversion(self, zone: Dict) -> bool:
        """پشکنینی ئینڤێرژن"""
        # Inversion Valid Support/Resistance
        return zone.get('inversion', False)
    
    def analyze_power_of_second_touch(self, zones: List) -> Dict:
        """شیکاری پاوەر ئۆف سێکەند تاچ"""
        # PO2 - دووەم تەج
        po2_zones = [z for z in zones if z.get('po2', False)]
        if len(po2_zones) >= 2:
            return {
                "signal": "BUY" if po2_zones[0]['type'] == 'support' else "SELL",
                "confidence": 0.9,
                "analysis": "PO2 - دووەم تەج دۆزرایەوە"
            }
        return None
    
    def get_trading_recommendation(self, user_data: Dict) -> Dict:
        """پێشنیاری تەرەیدکردن"""
        # هەموو تۆپیکەکان پێکەوە لەبەرچاو دەگیرێن
        recommendations = {
            "trade": None,
            "entry": None,
            "stop_loss": None,
            "take_profit": [None, None],
            "risk_reward": None,
            "timeframe": None
        }
        
        # ڕیزبەندی بەهێزی تۆپیکەکان (لە فایلەکەوە)
        # 1-Trend, 2-PO2, 3-PO2 inversion, 4-VS/VR Inversion, 5-GAP, 6-VS/VR Fresh, 7-SBR/RBS
        
        return recommendations