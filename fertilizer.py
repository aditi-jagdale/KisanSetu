import os
import random
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "kisansetu")
COLLECTION_NAME = "fertilizers"

_client: Optional[MongoClient] = None

def get_db():
    global _client
    if _client is None:
        if not MONGO_URI:
            raise ValueError("MONGO_URI is missing in .env")
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client[DB_NAME]

def _seed_records() -> List[Dict[str, Any]]:
    base_fertilizers = [
        {"name": "Urea", "type": "Chemical", "nutrient": "46% N", "form": "Granular", "pack_size": "45 kg", "base_price": 266, "trend": "+1.2%", "brand": "IFFCO"},
        {"name": "DAP", "type": "Chemical", "nutrient": "18% N, 46% P2O5", "form": "Granular", "pack_size": "50 kg", "base_price": 1350, "trend": "+0.8%", "brand": "Coromandel"},
        {"name": "MOP", "type": "Chemical", "nutrient": "60% K2O", "form": "Granular", "pack_size": "50 kg", "base_price": 1200, "trend": "-0.5%", "brand": "Chambal Fertilisers"},
        {"name": "SSP", "type": "Chemical", "nutrient": "16% P2O5", "form": "Granular", "pack_size": "50 kg", "base_price": 450, "trend": "+0.0%", "brand": "Rashtriya Chemicals"},
        {"name": "NPK 19:19:19", "type": "Chemical", "nutrient": "19% N, 19% P2O5, 19% K2O", "form": "Granular", "pack_size": "50 kg", "base_price": 1100, "trend": "+1.1%", "brand": "Nagarjuna"},
        {"name": "Vermicompost", "type": "Organic", "nutrient": "Organic Matter", "form": "Powder", "pack_size": "25 kg", "base_price": 350, "trend": "-0.3%", "brand": "Local Organic"},
        {"name": "Neem Cake", "type": "Organic", "nutrient": "Organic Matter, N", "form": "Powder", "pack_size": "25 kg", "base_price": 280, "trend": "-0.6%", "brand": "IFFCO"},
        {"name": "Bio NPK", "type": "Bio", "nutrient": "N, P, K & Micronutrients", "form": "Liquid", "pack_size": "1 L", "base_price": 220, "trend": "+0.7%", "brand": "Coromandel"},
        {"name": "Rhizobium", "type": "Bio", "nutrient": "Nitrogen Fixing", "form": "Liquid", "pack_size": "1 L", "base_price": 250, "trend": "+0.2%", "brand": "Rashtriya Chemicals"},
        {"name": "Zinc Sulfate", "type": "Micronutrients", "nutrient": "33% Zn, 15% S", "form": "Powder", "pack_size": "5 kg", "base_price": 400, "trend": "+1.5%", "brand": "Chambal Fertilisers"},
        {"name": "Boron 20%", "type": "Micronutrients", "nutrient": "20% B", "form": "Powder", "pack_size": "1 kg", "base_price": 150, "trend": "-0.1%", "brand": "Nagarjuna"},
        {"name": "Seaweed Extract", "type": "Organic", "nutrient": "Plant Growth Promoters", "form": "Liquid", "pack_size": "1 L", "base_price": 450, "trend": "+2.0%", "brand": "Local Organic"},
        {"name": "Ammonium Sulfate", "type": "Chemical", "nutrient": "21% N, 24% S", "form": "Granular", "pack_size": "50 kg", "base_price": 950, "trend": "+0.4%", "brand": "IFFCO"},
        {"name": "Calcium Nitrate", "type": "Chemical", "nutrient": "15.5% N, 18.8% Ca", "form": "Granular", "pack_size": "25 kg", "base_price": 1200, "trend": "-1.2%", "brand": "Coromandel"},
        {"name": "Mycorrhiza", "type": "Bio", "nutrient": "Phosphorus Mobilizing", "form": "Powder", "pack_size": "4 kg", "base_price": 380, "trend": "+0.5%", "brand": "Local Organic"},
    ]

    records = []
    
    brands = ["IFFCO", "Coromandel", "Chambal Fertilisers", "Rashtriya Chemicals", "Nagarjuna", "Local Organic"]
    
    # Generate ~150 combinations to populate the database
    for i in range(150):
        base = random.choice(base_fertilizers)
        variation = random.uniform(0.9, 1.1)
        price = int(base["base_price"] * variation)
        price = round(price / 5) * 5 # Round to nearest 5
        
        change_val = random.uniform(-2.0, 2.0)
        change_str = f"+{change_val:.1f}%" if change_val > 0 else f"{change_val:.1f}%"
        
        # Keep original brand mostly, but mix it up occasionally
        brand = base["brand"] if random.random() > 0.3 else random.choice(brands)
        
        # Slight variation in names to make them look like distinct products
        name_modifiers = ["Gold", "Premium", "Plus", "Super", "Max"]
        name = base["name"]
        if random.random() > 0.7:
             name = f"{name} {random.choice(name_modifiers)}"
             
        # Add primary nutrient classification for filters
        primary_nutrient = "Other"
        if "N" in base["nutrient"] and "P" not in base["nutrient"] and "K" not in base["nutrient"]:
            primary_nutrient = "Nitrogen"
        elif "P" in base["nutrient"] and "N" not in base["nutrient"]:
            primary_nutrient = "Phosphorus"
        elif "K" in base["nutrient"]:
            primary_nutrient = "Potassium"
        elif "Bio" in base["type"]:
             primary_nutrient = "Bio"
        elif "Organic" in base["type"]:
             primary_nutrient = "Organic"
             
        record = {
            "name": name,
            "type": base["type"],
            "nutrient_composition": base["nutrient"],
            "primary_nutrient": primary_nutrient,
            "form": base["form"],
            "pack_size": base["pack_size"],
            "price": price,
            "trend": change_str,
            "brand": brand
        }
        
        records.append(record)
        
    return records

def seed_fertilizer_data() -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]

    records = _seed_records()
    
    # Clear existing to avoid duplicates on reload
    collection.delete_many({})
    
    if records:
        collection.insert_many(records)
        print(f"Successfully seeded {len(records)} fertilizer records into MongoDB.")

def get_fertilizers(f_type: str = None, nutrient: str = None, form: str = None, brand: str = None, limit: int = 150) -> List[Dict[str, Any]]:
    db = get_db()
    collection = db[COLLECTION_NAME]

    query: Dict[str, Any] = {}
    if f_type and f_type != "All Types":
        query["type"] = f_type
    if nutrient and nutrient != "All Nutrients":
        query["primary_nutrient"] = nutrient
    if form and form != "All Forms":
        query["form"] = form
    if brand and brand != "All Brands":
        query["brand"] = brand

    cursor = collection.find(query).limit(limit)
    items: List[Dict[str, Any]] = []
    for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)

    return items

if __name__ == "__main__":
    seed_fertilizer_data()
