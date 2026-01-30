"""
Baumann Skin Type System + Weather Modifier

The 16 Baumann types are determined by 4 axes:
- D/O: Dry vs Oily
- S/R: Sensitive vs Resistant  
- P/N: Pigmented vs Non-pigmented
- W/T: Wrinkle-prone vs Tight

Weather modifiers adjust the effective skin behavior based on:
- Humidity (low = skin acts drier, high = skin acts oilier)
- Temperature (cold = more sensitive, hot = more oily)
- UV Index (high = more pigmentation risk)
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass

# Turkish city climate profiles with coordinates for live weather
TURKISH_CITIES = {
    "ankara": {
        "name": "Ankara",
        "lat": 39.9334,
        "lon": 32.8597,
        "climate": "continental_dry",
        "avg_humidity": 55,
        "avg_temp_summer": 30,
        "avg_temp_winter": 2,
        "notes": "Very dry winters, hot summers"
    },
    "istanbul": {
        "name": "İstanbul", 
        "lat": 41.0082,
        "lon": 28.9784,
        "climate": "humid_maritime",
        "avg_humidity": 73,
        "avg_temp_summer": 27,
        "avg_temp_winter": 6,
        "notes": "Humid year-round, mild temps"
    },
    "izmir": {
        "name": "İzmir",
        "lat": 38.4237,
        "lon": 27.1428,
        "climate": "mediterranean",
        "avg_humidity": 62,
        "avg_temp_summer": 33,
        "avg_temp_winter": 9,
        "notes": "Hot dry summers, mild wet winters"
    },
    "antalya": {
        "name": "Antalya",
        "lat": 36.8969,
        "lon": 30.7133,
        "climate": "mediterranean_coastal",
        "avg_humidity": 64,
        "avg_temp_summer": 34,
        "avg_temp_winter": 10,
        "notes": "Hot humid coastal climate"
    },
    "bursa": {
        "name": "Bursa",
        "lat": 40.1885,
        "lon": 29.0610,
        "climate": "transitional",
        "avg_humidity": 68,
        "avg_temp_summer": 29,
        "avg_temp_winter": 5,
        "notes": "Between maritime and continental"
    },
    "adana": {
        "name": "Adana",
        "lat": 37.0000,
        "lon": 35.3213,
        "climate": "mediterranean_hot",
        "avg_humidity": 66,
        "avg_temp_summer": 35,
        "avg_temp_winter": 10,
        "notes": "Very hot summers, humid"
    },
    "gaziantep": {
        "name": "Gaziantep",
        "lat": 37.0662,
        "lon": 37.3833,
        "climate": "continental",
        "avg_humidity": 52,
        "avg_temp_summer": 32,
        "avg_temp_winter": 3,
        "notes": "Dry continental, cold winters"
    },
    "konya": {
        "name": "Konya",
        "lat": 37.8746,
        "lon": 32.4932,
        "climate": "continental_dry",
        "avg_humidity": 50,
        "avg_temp_summer": 30,
        "avg_temp_winter": 0,
        "notes": "Very dry, extreme temps"
    },
    "diyarbakir": {
        "name": "Diyarbakır",
        "lat": 37.9144,
        "lon": 40.2306,
        "climate": "continental_hot",
        "avg_humidity": 45,
        "avg_temp_summer": 38,
        "avg_temp_winter": 2,
        "notes": "Very hot dry summers"
    },
    "trabzon": {
        "name": "Trabzon",
        "lat": 41.0027,
        "lon": 39.7168,
        "climate": "humid_subtropical",
        "avg_humidity": 78,
        "avg_temp_summer": 26,
        "avg_temp_winter": 8,
        "notes": "Very humid Black Sea coast"
    },
    "samsun": {
        "name": "Samsun",
        "lat": 41.2867,
        "lon": 36.33,
        "climate": "humid_subtropical",
        "avg_humidity": 75,
        "avg_temp_summer": 26,
        "avg_temp_winter": 7,
        "notes": "Humid Black Sea climate"
    },
    "mersin": {
        "name": "Mersin",
        "lat": 36.8121,
        "lon": 34.6415,
        "climate": "mediterranean_coastal",
        "avg_humidity": 68,
        "avg_temp_summer": 33,
        "avg_temp_winter": 11,
        "notes": "Hot Mediterranean coast"
    }
}


@dataclass
class BaumannScore:
    """Raw Baumann axis scores (0-100)"""
    oily: int      # 0 = very dry, 100 = very oily
    sensitive: int # 0 = resistant, 100 = very sensitive
    pigmented: int # 0 = non-pigmented, 100 = highly pigmented
    wrinkle: int   # 0 = tight, 100 = wrinkle-prone
    
    def get_code(self) -> str:
        """Convert scores to 4-letter Baumann code"""
        d_o = "O" if self.oily >= 50 else "D"
        s_r = "S" if self.sensitive >= 50 else "R"
        p_n = "P" if self.pigmented >= 50 else "N"
        w_t = "W" if self.wrinkle >= 50 else "T"
        return f"{d_o}{s_r}{p_n}{w_t}"
    
    def get_description(self) -> Dict:
        """Get human-readable description"""
        code = self.get_code()
        return {
            "code": code,
            "oily_dry": "Oily" if self.oily >= 50 else "Dry",
            "sensitive_resistant": "Sensitive" if self.sensitive >= 50 else "Resistant",
            "pigmented": "Pigmented" if self.pigmented >= 50 else "Non-pigmented",
            "wrinkle": "Wrinkle-prone" if self.wrinkle >= 50 else "Tight"
        }


@dataclass
class WeatherData:
    """Current weather conditions"""
    humidity: int        # 0-100%
    temperature: float   # Celsius
    uv_index: float      # 0-11+
    city: Optional[str] = None
    

def calculate_weather_modifier(weather: WeatherData) -> Dict[str, int]:
    """
    Calculate how weather shifts each Baumann axis.
    Returns modifier values (-30 to +30) for each axis.
    """
    modifiers = {
        "oily": 0,
        "sensitive": 0,
        "pigmented": 0,
        "wrinkle": 0
    }
    
    # HUMIDITY affects oiliness
    # Low humidity (<40%) = skin acts drier (-20)
    # High humidity (>70%) = skin acts oilier (+20)
    if weather.humidity < 30:
        modifiers["oily"] = -25
    elif weather.humidity < 40:
        modifiers["oily"] = -15
    elif weather.humidity > 80:
        modifiers["oily"] = +20
    elif weather.humidity > 70:
        modifiers["oily"] = +10
    
    # TEMPERATURE affects sensitivity and oiliness
    # Cold (<10°C) = more sensitive, less oily
    # Hot (>30°C) = more oily, more sensitive (heat rash)
    if weather.temperature < 5:
        modifiers["sensitive"] += 15
        modifiers["oily"] -= 10
    elif weather.temperature < 10:
        modifiers["sensitive"] += 10
        modifiers["oily"] -= 5
    elif weather.temperature > 35:
        modifiers["oily"] += 15
        modifiers["sensitive"] += 10
    elif weather.temperature > 30:
        modifiers["oily"] += 10
        modifiers["sensitive"] += 5
    
    # UV INDEX affects pigmentation risk
    # High UV = increased pigmentation risk
    if weather.uv_index >= 8:
        modifiers["pigmented"] = +25
    elif weather.uv_index >= 6:
        modifiers["pigmented"] = +15
    elif weather.uv_index >= 3:
        modifiers["pigmented"] = +5
    
    return modifiers


def apply_weather_modifier(base_score: BaumannScore, weather: WeatherData) -> BaumannScore:
    """
    Apply weather modifiers to get the EFFECTIVE skin type.
    This is what your skin ACTS like in current conditions.
    """
    modifiers = calculate_weather_modifier(weather)
    
    # Apply modifiers and clamp to 0-100
    adjusted = BaumannScore(
        oily=max(0, min(100, base_score.oily + modifiers["oily"])),
        sensitive=max(0, min(100, base_score.sensitive + modifiers["sensitive"])),
        pigmented=max(0, min(100, base_score.pigmented + modifiers["pigmented"])),
        wrinkle=base_score.wrinkle + modifiers["wrinkle"]  # wrinkle less affected by weather
    )
    
    return adjusted


# Quiz questions for determining Baumann type
BAUMANN_QUIZ = [
    {
        "id": 1,
        "axis": "oily",
        "question": "Yüzünüzü yıkadıktan 2-3 saat sonra cildiniz nasıl hissediyor?",
        "question_en": "How does your face feel 2-3 hours after washing?",
        "answers": [
            {"text": "Çok gergin ve kuru", "text_en": "Very tight and dry", "score": 10},
            {"text": "Biraz kuru", "text_en": "Slightly dry", "score": 30},
            {"text": "Normal, rahat", "text_en": "Normal, comfortable", "score": 50},
            {"text": "T-bölgede hafif yağlı", "text_en": "Slightly oily in T-zone", "score": 70},
            {"text": "Her yerde yağlı ve parlak", "text_en": "Oily and shiny everywhere", "score": 90}
        ]
    },
    {
        "id": 2,
        "axis": "oily",
        "question": "Gözenekleriniz nasıl görünüyor?",
        "question_en": "How do your pores look?",
        "answers": [
            {"text": "Neredeyse görünmez", "text_en": "Almost invisible", "score": 10},
            {"text": "Küçük, sadece burunda görünür", "text_en": "Small, visible only on nose", "score": 40},
            {"text": "Orta büyüklükte", "text_en": "Medium-sized", "score": 60},
            {"text": "Büyük ve belirgin", "text_en": "Large and visible", "score": 90}
        ]
    },
    {
        "id": 3,
        "axis": "sensitive",
        "question": "Yeni ürünlere cildiniz nasıl tepki veriyor?",
        "question_en": "How does your skin react to new products?",
        "answers": [
            {"text": "Hiç sorun yaşamam", "text_en": "Never have issues", "score": 10},
            {"text": "Nadiren kızarıklık olur", "text_en": "Rarely get redness", "score": 30},
            {"text": "Bazen tahriş olur", "text_en": "Sometimes get irritated", "score": 60},
            {"text": "Sık sık kızarır, kaşınır veya yanar", "text_en": "Often get red, itchy or burning", "score": 90}
        ]
    },
    {
        "id": 4,
        "axis": "sensitive",
        "question": "Güneşte cildiniz nasıl tepki verir?",
        "question_en": "How does your skin react in the sun?",
        "answers": [
            {"text": "Kolayca bronzlaşırım, yanmam", "text_en": "Tan easily, never burn", "score": 10},
            {"text": "Önce hafif yanarım, sonra bronzlaşırım", "text_en": "Burn slightly first, then tan", "score": 40},
            {"text": "Sık sık yanarım", "text_en": "Burn frequently", "score": 70},
            {"text": "Çok kolay yanarım, bronzlaşamam", "text_en": "Burn very easily, can't tan", "score": 90}
        ]
    },
    {
        "id": 5,
        "axis": "pigmented",
        "question": "Sivilce veya yaralanma sonrası cildinizde leke kalır mı?",
        "question_en": "Do you get dark spots after acne or injury?",
        "answers": [
            {"text": "Hayır, hiç iz kalmaz", "text_en": "No, no marks left", "score": 10},
            {"text": "Nadiren, hemen geçer", "text_en": "Rarely, fades quickly", "score": 30},
            {"text": "Bazen, birkaç hafta sürer", "text_en": "Sometimes, lasts few weeks", "score": 60},
            {"text": "Evet, koyu lekeler aylarca kalır", "text_en": "Yes, dark spots last months", "score": 90}
        ]
    },
    {
        "id": 6,
        "axis": "wrinkle",
        "question": "Ailenizde erken yaşta kırışıklık var mı?",
        "question_en": "Does your family have early wrinkles?",
        "answers": [
            {"text": "Hayır, ailem genç görünür", "text_en": "No, family looks young", "score": 10},
            {"text": "Normal yaşlanma", "text_en": "Normal aging", "score": 40},
            {"text": "Biraz erken kırışıklık", "text_en": "Somewhat early wrinkles", "score": 60},
            {"text": "Evet, erken ve belirgin kırışıklıklar", "text_en": "Yes, early prominent wrinkles", "score": 90}
        ]
    }
]


def calculate_baumann_from_quiz(answers: Dict[int, int]) -> BaumannScore:
    """
    Calculate Baumann score from quiz answers.
    answers: dict of question_id -> selected score
    """
    # Group answers by axis
    axis_scores = {
        "oily": [],
        "sensitive": [],
        "pigmented": [],
        "wrinkle": []
    }
    
    for q in BAUMANN_QUIZ:
        q_id = q["id"]
        if q_id in answers:
            axis_scores[q["axis"]].append(answers[q_id])
    
    # Average each axis
    def avg(scores):
        return int(sum(scores) / len(scores)) if scores else 50
    
    return BaumannScore(
        oily=avg(axis_scores["oily"]),
        sensitive=avg(axis_scores["sensitive"]),
        pigmented=avg(axis_scores["pigmented"]),
        wrinkle=avg(axis_scores["wrinkle"])
    )


def get_skincare_priorities(adjusted_score: BaumannScore, weather: WeatherData) -> list:
    """
    Get prioritized skincare concerns based on adjusted skin type.
    """
    priorities = []
    
    # Oily/Dry axis
    if adjusted_score.oily >= 70:
        priorities.append({
            "concern": "excess_oil",
            "priority": "high",
            "recommendation_tr": "Yağ kontrolü ve gözenek temizliği öncelikli",
            "recommendation_en": "Focus on oil control and pore cleansing"
        })
    elif adjusted_score.oily <= 30:
        priorities.append({
            "concern": "dryness",
            "priority": "high", 
            "recommendation_tr": "Yoğun nemlendirme ve bariyer onarımı",
            "recommendation_en": "Intense hydration and barrier repair"
        })
    
    # Sensitivity
    if adjusted_score.sensitive >= 70:
        priorities.append({
            "concern": "sensitivity",
            "priority": "high",
            "recommendation_tr": "Yatıştırıcı ve parfümsüz ürünler kullanın",
            "recommendation_en": "Use soothing, fragrance-free products"
        })
    
    # Pigmentation (especially if high UV)
    if adjusted_score.pigmented >= 60 or weather.uv_index >= 5:
        priorities.append({
            "concern": "pigmentation",
            "priority": "high" if weather.uv_index >= 6 else "medium",
            "recommendation_tr": "Güneş koruması ve leke karşıtı aktifler",
            "recommendation_en": "Sun protection and anti-spot actives"
        })
    
    # Wrinkle
    if adjusted_score.wrinkle >= 60:
        priorities.append({
            "concern": "aging",
            "priority": "medium",
            "recommendation_tr": "Anti-aging aktifler ve antioksidanlar",
            "recommendation_en": "Anti-aging actives and antioxidants"
        })
    
    # Weather-specific
    if weather.humidity < 40:
        priorities.append({
            "concern": "dehydration",
            "priority": "high",
            "recommendation_tr": "Hava çok kuru - ekstra nemlendirme gerekli",
            "recommendation_en": "Air is very dry - extra hydration needed"
        })
    
    return priorities
