import os
import random
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "kisansetu")
COLLECTION_NAME = "market_prices"

_client: Optional[MongoClient] = None

def get_db():
    global _client
    if _client is None:
        if not MONGO_URI:
            raise ValueError("MONGO_URI is missing in .env")
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client[DB_NAME]

def _generate_trend_data(base_price: int) -> List[int]:
    """Generates 7 days of realistic trend data centered around a base price."""
    trend = []
    current_price = base_price - random.randint(-100, 100) # Start slightly off base
    for _ in range(7):
        # Fluctuate by -2% to +2%
        change = current_price * random.uniform(-0.02, 0.02)
        current_price += int(change)
        trend.append(current_price)
    # Ensure the last day is exactly the base_price to match the modal price
    trend[-1] = base_price
    return trend

def _seed_records() -> List[Dict[str, Any]]:
    crops = [
        {"name": "Wheat", "base": 2300, "icon": "https://cdn-icons-png.flaticon.com/512/5024/5024479.png"},
        {"name": "Rice (Paddy)", "base": 2050, "icon": "https://cdn-icons-png.flaticon.com/512/3014/3014495.png"},
        {"name": "Cotton", "base": 5800, "icon": "https://cdn-icons-png.flaticon.com/512/3061/3061189.png"},
        {"name": "Maize", "base": 620, "icon": "https://cdn-icons-png.flaticon.com/512/1206/1206385.png"},
        {"name": "Tur (Pigeon Pea)", "base": 7150, "icon": "https://cdn-icons-png.flaticon.com/512/3221/3221976.png"},
        {"name": "Tomato", "base": 1200, "icon": "https://cdn-icons-png.flaticon.com/512/1206/1206363.png"},
        {"name": "Potato", "base": 800, "icon": "https://cdn-icons-png.flaticon.com/512/1135/1135548.png"},
        {"name": "Onion", "base": 1500, "icon": "https://cdn-icons-png.flaticon.com/512/1135/1135552.png"},
        {"name": "Soybean", "base": 4500, "icon": "https://cdn-icons-png.flaticon.com/512/10363/10363065.png"},
        {"name": "Sugarcane", "base": 315, "icon": "https://cdn-icons-png.flaticon.com/512/6122/6122171.png"},
        {"name": "Saffron", "base": 8750, "icon": "https://cdn-icons-png.flaticon.com/512/7594/7594611.png"},
        {"name": "Apple", "base": 6000, "icon": "https://cdn-icons-png.flaticon.com/512/415/415682.png"},
        {"name": "Banana", "base": 1800, "icon": "https://cdn-icons-png.flaticon.com/512/2909/2909808.png"},
        {"name": "Grapes", "base": 3500, "icon": "https://cdn-icons-png.flaticon.com/512/1135/1135544.png"},
        {"name": "Mango", "base": 4000, "icon": "https://cdn-icons-png.flaticon.com/512/2909/2909890.png"},
        {"name": "Chilli", "base": 9000, "icon": "https://cdn-icons-png.flaticon.com/512/2909/2909819.png"},
        {"name": "Garlic", "base": 8500, "icon": "https://cdn-icons-png.flaticon.com/512/1135/1135546.png"},
        {"name": "Turmeric", "base": 7800, "icon": "https://cdn-icons-png.flaticon.com/512/6533/6533925.png"},
        {"name": "Ginger", "base": 6500, "icon": "https://cdn-icons-png.flaticon.com/512/7444/7444738.png"},
        {"name": "Mustard", "base": 5200, "icon": "https://cdn-icons-png.flaticon.com/512/6666/6666249.png"},
        {"name": "Groundnut", "base": 6200, "icon": "https://cdn-icons-png.flaticon.com/512/5024/5024479.png"},
        {"name": "Coffee", "base": 15000, "icon": "https://cdn-icons-png.flaticon.com/512/924/924514.png"},
        {"name": "Tea", "base": 12000, "icon": "https://cdn-icons-png.flaticon.com/512/1182/1182103.png"},
    ]

    markets_data = [
        {"market": "Azadpur Mandi", "state": "Delhi"},
        {"market": "Kalyan Mandi", "state": "Maharashtra"},
        {"market": "Rajkot Mandi", "state": "Gujarat"},
        {"market": "Patna Mandi", "state": "Bihar"},
        {"market": "Latur Mandi", "state": "Maharashtra"},
        {"market": "Karnal Mandi", "state": "Haryana"},
        {"market": "Ludhiana Mandi", "state": "Punjab"},
        {"market": "Indore Mandi", "state": "Madhya Pradesh"},
        {"market": "Kurnool Mandi", "state": "Andhra Pradesh"},
        {"market": "Vashi APMC", "state": "Maharashtra"},
        {"market": "Srinagar Mandi", "state": "Kashmir"},
        {"market": "Nashik Mandi", "state": "Maharashtra"},
        {"market": "Guntur Mandi", "state": "Andhra Pradesh"},
        {"market": "Hubli Mandi", "state": "Karnataka"},
        {"market": "Surat Mandi", "state": "Gujarat"},
        {"market": "Ahmedabad Mandi", "state": "Gujarat"},
        {"market": "Jaipur Mandi", "state": "Rajasthan"},
        {"market": "Jodhpur Mandi", "state": "Rajasthan"},
        {"market": "Lucknow Mandi", "state": "Uttar Pradesh"},
        {"market": "Agra Mandi", "state": "Uttar Pradesh"},
        {"market": "Kanpur Mandi", "state": "Uttar Pradesh"},
        {"market": "Shimla Mandi", "state": "Himachal Pradesh"},
        {"market": "Guwahati Mandi", "state": "Assam"},
        {"market": "Bhubaneswar Mandi", "state": "Odisha"},
        {"market": "Raipur Mandi", "state": "Chhattisgarh"},
        {"market": "Ranchi Mandi", "state": "Jharkhand"},
        {"market": "Dehradun Mandi", "state": "Uttarakhand"},
        {"market": "Kochi Mandi", "state": "Kerala"},
        {"market": "Madurai Mandi", "state": "Tamil Nadu"},
        {"market": "Coimbatore Mandi", "state": "Tamil Nadu"},
        {"market": "Kolkata Mandi", "state": "West Bengal"},
    ]

    records = []
    
    # Generate ~500 combinations
    for _ in range(500):
        crop = random.choice(crops)
        location = random.choice(markets_data)
        
        # Add some regional bias (e.g. Saffron is usually Kashmir)
        if crop["name"] == "Saffron":
            location = {"market": "Srinagar Mandi", "state": "Kashmir"}
        
        # Calculate realistic prices
        variation = random.uniform(0.8, 1.2) # Prices vary by market
        modal = int(crop["base"] * variation)
        # Round to nearest 10
        modal = round(modal / 10) * 10
        
        min_p = int(modal * 0.9)
        max_p = int(modal * 1.1)
        
        # Ensure min < modal < max
        if min_p >= modal: min_p = modal - 10
        if max_p <= modal: max_p = modal + 10
        
        change_val = random.uniform(-5.0, 5.0)
        change_str = f"+{change_val:.2f}%" if change_val > 0 else f"{change_val:.2f}%"
        
        trend = _generate_trend_data(modal)
        
        record = {
            "crop_name": crop["name"],
            "crop_icon": crop["icon"],
            "market": location["market"],
            "state": location["state"],
            "min_price": min_p,
            "max_price": max_p,
            "modal_price": modal,
            "change": change_str,
            "trend_data": trend, # 7 data points
            "date_updated": "Today"
        }
        
        # Ensure uniqueness in generation (we'll just append, MongoDB will handle bulk if we need unique)
        records.append(record)
        
    return records

def seed_market_data() -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]

    records = _seed_records()
    
    # Completely clear existing to avoid messy duplicates on reload
    collection.delete_many({})
    
    if records:
        collection.insert_many(records)
        print(f"Successfully seeded {len(records)} market records into MongoDB.")

def get_market_prices(crop: str = None, state: str = None, market: str = None, limit: int = 150) -> List[Dict[str, Any]]:
    db = get_db()
    collection = db[COLLECTION_NAME]

    query: Dict[str, Any] = {}
    if crop and crop != "All Crops":
        query["crop_name"] = crop
    if state and state != "All States":
        query["state"] = state
    if market and market != "All Markets":
        query["market"] = market

    cursor = collection.find(query).limit(limit)
    items: List[Dict[str, Any]] = []
    for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)

    return items

if __name__ == "__main__":
    seed_market_data()
