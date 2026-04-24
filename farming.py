import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "kisansetu")
COLLECTION_NAME = "farming_techniques"

_client: Optional[MongoClient] = None


def get_db():
    global _client
    if _client is None:
        if not MONGO_URI:
            raise ValueError("MONGO_URI is missing in .env")
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client[DB_NAME]


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _seed_records() -> List[Dict[str, Any]]:
    # Define techniques as seen in mockup
    techniques = [
        # Traditional Techniques
        {
            "title": "Crop Rotation",
            "category": "Traditional Techniques",
            "description": "Benefits for soil fertility and pest control.",
            "image": "https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Mixed Cropping & Intercropping",
            "category": "Traditional Techniques",
            "description": "Growing multiple crops together for resilience.",
            "image": "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Shifting Cultivation",
            "category": "Traditional Techniques",
            "description": "Historical practices and modern adaptations.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },

        # Modern & Mechanized
        {
            "title": "Precision Farming",
            "category": "Modern & Mechanized",
            "description": "Use of GPS, sensors, and drones for targeted input application.",
            "image": "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Mechanization",
            "category": "Modern & Mechanized",
            "description": "Tractors, harvesters, planters, and irrigation systems.",
            "image": "https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Hydroponics & Aeroponics",
            "category": "Modern & Mechanized",
            "description": "Soil-less farming methods for higher productivity.",
            "image": "https://images.unsplash.com/photo-1585860956976-58c0c05df756?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },

        # Sustainable & Eco-Friendly
        {
            "title": "Organic Farming",
            "category": "Sustainable & Eco-Friendly",
            "description": "Composting, biofertilizers, natural pest control.",
            "image": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Agroforestry",
            "category": "Sustainable & Eco-Friendly",
            "description": "Integrating trees with crops for biodiversity and soil health.",
            "image": "https://images.unsplash.com/photo-1501084817091-a4f3d1d19e07?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Conservation Tillage",
            "category": "Sustainable & Eco-Friendly",
            "description": "Reducing soil disturbance to preserve moisture and carbon.",
            "image": "https://images.unsplash.com/photo-1599839619722-39751411ea63?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Water-saving Methods",
            "category": "Sustainable & Eco-Friendly",
            "description": "Drip irrigation, rainwater harvesting for efficient water use.",
            "image": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },

        # Innovative & Emerging
        {
            "title": "Vertical Farming",
            "category": "Innovative & Emerging",
            "description": "Urban and space-efficient food production.",
            "image": "https://images.unsplash.com/photo-1530836369250-ef71a3f5e481?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Genetically Improved Seeds",
            "category": "Innovative & Emerging",
            "description": "Drought-resistant, pest-resistant varieties.",
            "image": "https://images.unsplash.com/photo-1628189874795-09bd2925b3ea?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Climate-smart Agriculture",
            "category": "Innovative & Emerging",
            "description": "Practices adapted to changing weather patterns.",
            "image": "https://images.unsplash.com/photo-1585860956976-58c0c05df756?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },
        {
            "title": "Smart Farming Tools",
            "category": "Innovative & Emerging",
            "description": "AI, IoT, and mobile apps for monitoring and decision-making.",
            "image": "https://images.unsplash.com/photo-1532629345422-7515f3d16bb0?auto=format&fit=crop&w=600&q=80",
            "type": "image"
        },

        # Practical Guides
        {
            "title": "Step-by-step Manuals",
            "category": "Practical Guides",
            "description": "How to implement each technique.",
            "icon": "fa-clipboard-list",
            "type": "icon"
        },
        {
            "title": "Cost-benefit Analysis",
            "category": "Practical Guides",
            "description": "Comparing traditional vs modern methods.",
            "icon": "fa-chart-line",
            "type": "icon"
        },
        {
            "title": "Case Studies",
            "category": "Practical Guides",
            "description": "Success stories from different regions.",
            "icon": "fa-map-location-dot",
            "type": "icon"
        },

        # Farmer Support
        {
            "title": "Training Modules",
            "category": "Farmer Support",
            "description": "Videos, infographics, and workshops.",
            "icon": "fa-person-chalkboard",
            "type": "icon"
        },
        {
            "title": "Government Schemes",
            "category": "Farmer Support",
            "description": "Subsidies for adopting new techniques.",
            "icon": "fa-building-columns",
            "type": "icon"
        },
        {
            "title": "Community Sharing",
            "category": "Farmer Support",
            "description": "Forums and farmer networks.",
            "icon": "fa-users-viewfinder",
            "type": "icon"
        }
    ]

    records: List[Dict[str, Any]] = []
    for item in techniques:
        item["slug"] = _slugify(item["title"])
        records.append(item)

    return records


def seed_farming_data() -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]

    records = _seed_records()
    operations = []
    valid_slugs = []
    for record in records:
        slug = record["slug"]
        valid_slugs.append(slug)
        operations.append(
            UpdateOne(
                {"slug": slug},
                {"$set": record},
                upsert=True,
            )
        )

    if operations:
        collection.bulk_write(operations, ordered=False)
    collection.delete_many({"slug": {"$nin": valid_slugs}})
    collection.create_index("slug", unique=True)
    collection.create_index("category")


def get_techniques() -> List[Dict[str, Any]]:
    db = get_db()
    collection = db[COLLECTION_NAME]
    
    cursor = collection.find({})
    items: List[Dict[str, Any]] = []
    for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)

    return items
