import cv2
import numpy as np
from PIL import Image
import pytesseract
import tensorflow as tf
from typing import Dict, List, Tuple

class ImageProcessor:
    def __init__(self):
        self.model = self._load_model()
        
    def _load_model(self):
        """بارکردنی مۆدێلی فێربوونی مەکینە بۆ ناسینی زۆنەکان"""
        # بەکارهێنانی مۆدێلی پێش-ڕاهێنراو بۆ ناسینی شێوە
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        شیکاری وێنەی چارت
        
        Returns:
            {
                "zones": {
                    "sell_zones": [{"level": 2200, "timeframe": "1h", "type": "resistance"}],
                    "buy_zones": [{"level": 2100, "timeframe": "1h", "type": "support"}]
                },
                "patterns": ["SBR", "RBS", "SRR", "RSS"],
                "valid_zones": ["VS", "VR"],
                "inversions": ["IVS", "IVR"],
                "po2_detected": True,
                "gap_detected": False
            }
        """
        # خوێندنەوەی وێنە
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "وێنە نەدۆزرایەوە"}
        
        # گۆڕینی ڕەنگ بۆ خۆڵەمێشی
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # دۆزینەوەی هێڵەکان (سەپۆرت و ڕیسرستانس)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        
        zones = self._extract_zones_from_lines(lines, image.shape)
        
        # ناسینی تۆپیکەکانی SNRZ
        patterns = self._detect_snrz_patterns(image, gray)
        
        # شیکاری PO2
        po2_detected = self._detect_po2(image)
        
        return {
            "zones": zones,
            "patterns": patterns,
            "valid_zones": self._detect_valid_zones(image),
            "inversions": self._detect_inversions(image),
            "po2_detected": po2_detected,
            "gap_detected": self._detect_gap(image)
        }
    
    def _extract_zones_from_lines(self, lines, image_shape) -> Dict:
        """هەڵگرتنی زۆنەکان لە هێڵەکان"""
        sell_zones = []
        buy_zones = []
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # شیکاری ئاراستەی هێڵ
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
                
                if slope < -0.5:  # هێڵی بەرەو خوارەوە
                    sell_zones.append({
                        "level": y1,
                        "type": "resistance",
                        "strength": 0.8
                    })
                elif slope > 0.5:  # هێڵی بەرەو سەرەوە
                    buy_zones.append({
                        "level": y1,
                        "type": "support",
                        "strength": 0.8
                    })
        
        return {"sell_zones": sell_zones, "buy_zones": buy_zones}
    
    def _detect_snrz_patterns(self, image, gray) -> List[str]:
        """ناسینی شێوەکانی SNRZ"""
        patterns = []
        # بەکارهێنانی OCR بۆ خوێندنەوەی تێکست
        text = pytesseract.image_to_string(gray, lang='eng+kur')
        
        # گەڕان بۆ کلیلە وشەکان
        keywords = ["SBR", "RBS", "SRR", "RSS", "VS", "VR", "IVS", "IVR", "PO2"]
        for keyword in keywords:
            if keyword in text.upper():
                patterns.append(keyword)
        
        return patterns
    
    def _detect_valid_zones(self, image) -> List[str]:
        """ناسینی ڤالید زۆنەکان"""
        # شیکاری قوڵایی زۆنەکان
        return []
    
    def _detect_inversions(self, image) -> List[str]:
        """ناسینی ئینڤێرژنەکان"""
        return []
    
    def _detect_po2(self, image) -> bool:
        """ناسینی PO2"""
        return False
    
    def _detect_gap(self, image) -> bool:
        """ناسینی GAP"""
        return False