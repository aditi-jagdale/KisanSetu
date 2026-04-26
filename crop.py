import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "kisansetu")
COLLECTION_NAME = "crops"
TARGET_CROP_COUNT = 520

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


def _build_image_url(query: str) -> str:
    safe_query = query.replace(' ', '%20')
    # Using Bing's dynamic thumbnail generator which acts as a reliable Google Images alternative
    return f'https://tse1.mm.bing.net/th?q={safe_query}%20crop%20plant&w=400&h=400&c=7&rs=1&p=0&dpr=1&pid=1.7'

def _seed_records() -> List[Dict[str, Any]]:
    base_crops = [
        {"name": "Rice", "scientific_name": "Oryza sativa", "family": "Poaceae", "category": "Cereals", "local_names": "Dhan, Chawal"},
        {"name": "Wheat", "scientific_name": "Triticum aestivum", "family": "Poaceae", "category": "Cereals", "local_names": "Gehun"},
        {"name": "Maize", "scientific_name": "Zea mays", "family": "Poaceae", "category": "Cereals", "local_names": "Makka"},
        {"name": "Barley", "scientific_name": "Hordeum vulgare", "family": "Poaceae", "category": "Cereals", "local_names": "Jau"},
        {"name": "Sorghum", "scientific_name": "Sorghum bicolor", "family": "Poaceae", "category": "Cereals", "local_names": "Jowar"},
        {"name": "Pearl Millet", "scientific_name": "Pennisetum glaucum", "family": "Poaceae", "category": "Cereals", "local_names": "Bajra"},
        {"name": "Finger Millet", "scientific_name": "Eleusine coracana", "family": "Poaceae", "category": "Cereals", "local_names": "Ragi"},
        {"name": "Foxtail Millet", "scientific_name": "Setaria italica", "family": "Poaceae", "category": "Cereals", "local_names": "Kangni"},
        {"name": "Kodo Millet", "scientific_name": "Paspalum scrobiculatum", "family": "Poaceae", "category": "Cereals", "local_names": "Kodon"},
        {"name": "Little Millet", "scientific_name": "Panicum sumatrense", "family": "Poaceae", "category": "Cereals", "local_names": "Kutki"},
        {"name": "Chickpea", "scientific_name": "Cicer arietinum", "family": "Fabaceae", "category": "Pulses", "local_names": "Chana"},
        {"name": "Pigeon Pea", "scientific_name": "Cajanus cajan", "family": "Fabaceae", "category": "Pulses", "local_names": "Arhar"},
        {"name": "Green Gram", "scientific_name": "Vigna radiata", "family": "Fabaceae", "category": "Pulses", "local_names": "Moong"},
        {"name": "Black Gram", "scientific_name": "Vigna mungo", "family": "Fabaceae", "category": "Pulses", "local_names": "Urad"},
        {"name": "Lentil", "scientific_name": "Lens culinaris", "family": "Fabaceae", "category": "Pulses", "local_names": "Masoor"},
        {"name": "Field Pea", "scientific_name": "Pisum sativum", "family": "Fabaceae", "category": "Pulses", "local_names": "Matar"},
        {"name": "Cowpea", "scientific_name": "Vigna unguiculata", "family": "Fabaceae", "category": "Pulses", "local_names": "Lobia"},
        {"name": "Horse Gram", "scientific_name": "Macrotyloma uniflorum", "family": "Fabaceae", "category": "Pulses", "local_names": "Kulthi"},
        {"name": "Moth Bean", "scientific_name": "Vigna aconitifolia", "family": "Fabaceae", "category": "Pulses", "local_names": "Matki"},
        {"name": "Rajma", "scientific_name": "Phaseolus vulgaris", "family": "Fabaceae", "category": "Pulses", "local_names": "Rajma"},
        {"name": "Groundnut", "scientific_name": "Arachis hypogaea", "family": "Fabaceae", "category": "Oilseeds", "local_names": "Mungfali"},
        {"name": "Mustard", "scientific_name": "Brassica juncea", "family": "Brassicaceae", "category": "Oilseeds", "local_names": "Sarson"},
        {"name": "Rapeseed", "scientific_name": "Brassica napus", "family": "Brassicaceae", "category": "Oilseeds", "local_names": "Toria"},
        {"name": "Sesame", "scientific_name": "Sesamum indicum", "family": "Pedaliaceae", "category": "Oilseeds", "local_names": "Til"},
        {"name": "Sunflower", "scientific_name": "Helianthus annuus", "family": "Asteraceae", "category": "Oilseeds", "local_names": "Surajmukhi"},
        {"name": "Safflower", "scientific_name": "Carthamus tinctorius", "family": "Asteraceae", "category": "Oilseeds", "local_names": "Kusum"},
        {"name": "Linseed", "scientific_name": "Linum usitatissimum", "family": "Linaceae", "category": "Oilseeds", "local_names": "Alsi"},
        {"name": "Castor", "scientific_name": "Ricinus communis", "family": "Euphorbiaceae", "category": "Oilseeds", "local_names": "Arandi"},
        {"name": "Soybean", "scientific_name": "Glycine max", "family": "Fabaceae", "category": "Oilseeds", "local_names": "Soyabean"},
        {"name": "Niger", "scientific_name": "Guizotia abyssinica", "family": "Asteraceae", "category": "Oilseeds", "local_names": "Ramtil"},
        {"name": "Tomato", "scientific_name": "Solanum lycopersicum", "family": "Solanaceae", "category": "Vegetables", "local_names": "Tamatar"},
        {"name": "Potato", "scientific_name": "Solanum tuberosum", "family": "Solanaceae", "category": "Vegetables", "local_names": "Aloo"},
        {"name": "Onion", "scientific_name": "Allium cepa", "family": "Amaryllidaceae", "category": "Vegetables", "local_names": "Pyaz"},
        {"name": "Garlic", "scientific_name": "Allium sativum", "family": "Amaryllidaceae", "category": "Vegetables", "local_names": "Lahsun"},
        {"name": "Brinjal", "scientific_name": "Solanum melongena", "family": "Solanaceae", "category": "Vegetables", "local_names": "Baingan"},
        {"name": "Cabbage", "scientific_name": "Brassica oleracea var. capitata", "family": "Brassicaceae", "category": "Vegetables", "local_names": "Patta Gobhi"},
        {"name": "Cauliflower", "scientific_name": "Brassica oleracea var. botrytis", "family": "Brassicaceae", "category": "Vegetables", "local_names": "Phool Gobhi"},
        {"name": "Okra", "scientific_name": "Abelmoschus esculentus", "family": "Malvaceae", "category": "Vegetables", "local_names": "Bhindi"},
        {"name": "Pumpkin", "scientific_name": "Cucurbita maxima", "family": "Cucurbitaceae", "category": "Vegetables", "local_names": "Kaddu"},
        {"name": "Bottle Gourd", "scientific_name": "Lagenaria siceraria", "family": "Cucurbitaceae", "category": "Vegetables", "local_names": "Lauki"},
        {"name": "Bitter Gourd", "scientific_name": "Momordica charantia", "family": "Cucurbitaceae", "category": "Vegetables", "local_names": "Karela"},
        {"name": "Cucumber", "scientific_name": "Cucumis sativus", "family": "Cucurbitaceae", "category": "Vegetables", "local_names": "Kheera"},
        {"name": "Carrot", "scientific_name": "Daucus carota", "family": "Apiaceae", "category": "Vegetables", "local_names": "Gajar"},
        {"name": "Radish", "scientific_name": "Raphanus sativus", "family": "Brassicaceae", "category": "Vegetables", "local_names": "Mooli"},
        {"name": "Spinach", "scientific_name": "Spinacia oleracea", "family": "Amaranthaceae", "category": "Vegetables", "local_names": "Palak"},
        {"name": "Chilli", "scientific_name": "Capsicum annuum", "family": "Solanaceae", "category": "Vegetables", "local_names": "Mirch"},
        {"name": "Banana", "scientific_name": "Musa paradisiaca", "family": "Musaceae", "category": "Fruits", "local_names": "Kela"},
        {"name": "Mango", "scientific_name": "Mangifera indica", "family": "Anacardiaceae", "category": "Fruits", "local_names": "Aam"},
        {"name": "Papaya", "scientific_name": "Carica papaya", "family": "Caricaceae", "category": "Fruits", "local_names": "Papita"},
        {"name": "Guava", "scientific_name": "Psidium guajava", "family": "Myrtaceae", "category": "Fruits", "local_names": "Amrud"},
        {"name": "Pomegranate", "scientific_name": "Punica granatum", "family": "Lythraceae", "category": "Fruits", "local_names": "Anar"},
        {"name": "Orange", "scientific_name": "Citrus sinensis", "family": "Rutaceae", "category": "Fruits", "local_names": "Santra"},
        {"name": "Lemon", "scientific_name": "Citrus limon", "family": "Rutaceae", "category": "Fruits", "local_names": "Nimbu"},
        {"name": "Apple", "scientific_name": "Malus domestica", "family": "Rosaceae", "category": "Fruits", "local_names": "Seb"},
        {"name": "Grapes", "scientific_name": "Vitis vinifera", "family": "Vitaceae", "category": "Fruits", "local_names": "Angoor"},
        {"name": "Pineapple", "scientific_name": "Ananas comosus", "family": "Bromeliaceae", "category": "Fruits", "local_names": "Ananas"},
        {"name": "Turmeric", "scientific_name": "Curcuma longa", "family": "Zingiberaceae", "category": "Spices", "local_names": "Haldi"},
        {"name": "Ginger", "scientific_name": "Zingiber officinale", "family": "Zingiberaceae", "category": "Spices", "local_names": "Adrak"},
        {"name": "Coriander", "scientific_name": "Coriandrum sativum", "family": "Apiaceae", "category": "Spices", "local_names": "Dhaniya"},
        {"name": "Cumin", "scientific_name": "Cuminum cyminum", "family": "Apiaceae", "category": "Spices", "local_names": "Jeera"},
        {"name": "Fennel", "scientific_name": "Foeniculum vulgare", "family": "Apiaceae", "category": "Spices", "local_names": "Saunf"},
        {"name": "Fenugreek", "scientific_name": "Trigonella foenum-graecum", "family": "Fabaceae", "category": "Spices", "local_names": "Methi"},
        {"name": "Cardamom", "scientific_name": "Elettaria cardamomum", "family": "Zingiberaceae", "category": "Spices", "local_names": "Elaichi"},
        {"name": "Black Pepper", "scientific_name": "Piper nigrum", "family": "Piperaceae", "category": "Spices", "local_names": "Kali Mirch"},
        {"name": "Clove", "scientific_name": "Syzygium aromaticum", "family": "Myrtaceae", "category": "Spices", "local_names": "Laung"},
        {"name": "Cinnamon", "scientific_name": "Cinnamomum verum", "family": "Lauraceae", "category": "Spices", "local_names": "Dalchini"},
        {"name": "Sugarcane", "scientific_name": "Saccharum officinarum", "family": "Poaceae", "category": "Cash Crops", "local_names": "Ganna"},
        {"name": "Cotton", "scientific_name": "Gossypium hirsutum", "family": "Malvaceae", "category": "Cash Crops", "local_names": "Kapas"},
        {"name": "Jute", "scientific_name": "Corchorus olitorius", "family": "Malvaceae", "category": "Cash Crops", "local_names": "Pat"},
        {"name": "Tobacco", "scientific_name": "Nicotiana tabacum", "family": "Solanaceae", "category": "Cash Crops", "local_names": "Tambaku"},
        {"name": "Coffee", "scientific_name": "Coffea arabica", "family": "Rubiaceae", "category": "Plantation", "local_names": "Coffee"},
        {"name": "Tea", "scientific_name": "Camellia sinensis", "family": "Theaceae", "category": "Plantation", "local_names": "Chai"},
        {"name": "Rubber", "scientific_name": "Hevea brasiliensis", "family": "Euphorbiaceae", "category": "Plantation", "local_names": "Rubber"},
        {"name": "Coconut", "scientific_name": "Cocos nucifera", "family": "Arecaceae", "category": "Plantation", "local_names": "Nariyal"},
        {"name": "Arecanut", "scientific_name": "Areca catechu", "family": "Arecaceae", "category": "Plantation", "local_names": "Supari"},
        {"name": "Napier Grass", "scientific_name": "Cenchrus purpureus", "family": "Poaceae", "category": "Fodder Crops", "local_names": "Napier"},
        {"name": "Berseem", "scientific_name": "Trifolium alexandrinum", "family": "Fabaceae", "category": "Fodder Crops", "local_names": "Berseem"},
        {"name": "Lucerne", "scientific_name": "Medicago sativa", "family": "Fabaceae", "category": "Fodder Crops", "local_names": "Lucerne"},
        {"name": "Sunn Hemp", "scientific_name": "Crotalaria juncea", "family": "Fabaceae", "category": "Fibre Crops", "local_names": "San"},
        {"name": "Kenaf", "scientific_name": "Hibiscus cannabinus", "family": "Malvaceae", "category": "Fibre Crops", "local_names": "Kenaf"},
        {"name": "Roselle", "scientific_name": "Hibiscus sabdariffa", "family": "Malvaceae", "category": "Medicinal & Aromatic", "local_names": "Lal Ambadi"},
        {"name": "Aloe Vera", "scientific_name": "Aloe barbadensis miller", "family": "Asphodelaceae", "category": "Medicinal & Aromatic", "local_names": "Ghritkumari"},
        {"name": "Ashwagandha", "scientific_name": "Withania somnifera", "family": "Solanaceae", "category": "Medicinal & Aromatic", "local_names": "Asgandh"},
        {"name": "Mentha", "scientific_name": "Mentha arvensis", "family": "Lamiaceae", "category": "Medicinal & Aromatic", "local_names": "Pudina"},
        {"name": "Marigold", "scientific_name": "Tagetes erecta", "family": "Asteraceae", "category": "Floriculture", "local_names": "Genda"},
        {"name": "Rose", "scientific_name": "Rosa indica", "family": "Rosaceae", "category": "Floriculture", "local_names": "Gulab"},
        {"name": "Jasmine", "scientific_name": "Jasminum sambac", "family": "Oleaceae", "category": "Floriculture", "local_names": "Mogra"},
        {"name": "Cashew", "scientific_name": "Anacardium occidentale", "family": "Anacardiaceae", "category": "Nuts", "local_names": "Kaju"},
        {"name": "Almond", "scientific_name": "Prunus dulcis", "family": "Rosaceae", "category": "Nuts", "local_names": "Badam"},
        {"name": "Walnut", "scientific_name": "Juglans regia", "family": "Juglandaceae", "category": "Nuts", "local_names": "Akhrot"},
    ]

    season_cycle = ["Kharif", "Rabi", "Zaid", "Year-round"]
    climate_cycle = ["Tropical", "Sub-tropical", "Temperate", "Semi-arid"]
    irrigation_cycle = ["Drip irrigation", "Furrow irrigation", "Sprinkler irrigation", "Rainfed with supplemental irrigation"]
    soil_cycle = ["Well-drained loamy soil", "Sandy loam soil", "Clay loam soil", "Alluvial soil"]
    rainfall_cycle = ["400-700 mm", "600-900 mm", "800-1200 mm", "300-500 mm"]
    regions = ["North India", "South India", "East India", "West India", "Central India", "Himalayan Region"]

    records: List[Dict[str, Any]] = []
    idx = 0

    for base in base_crops:
        region = regions[idx % len(regions)]
        season = season_cycle[idx % len(season_cycle)]
        climate = climate_cycle[idx % len(climate_cycle)]
        irrigation = irrigation_cycle[idx % len(irrigation_cycle)]
        soil = soil_cycle[idx % len(soil_cycle)]
        rainfall = rainfall_cycle[idx % len(rainfall_cycle)]
        idx += 1

        display_name = base['name']
        slug = _slugify(display_name)

        records.append(
            {
                "slug": slug,
                "name": display_name,
                "base_crop": base["name"],
                "category": base["category"],
                "image": _build_image_url(base["name"]),
                "scientific_name": base["scientific_name"],
                "local_names": base["local_names"],
                "crop_family": base["family"],
                "native_region": region,
                "economic_importance": "High",
                "water_requirement": "Moderate",
                "growing_season": season,
                "basic_details": {
                    "scientific_name": base["scientific_name"],
                    "local_names": base["local_names"],
                    "crop_family": base["family"],
                },
                "overview": f"{base['name']} is widely grown in {region}. It thrives in {climate} climates with {soil}.",
                "varieties": {
                    "popular_cultivars": [
                        f"{base['name']} Classic",
                        f"{base['name']} Gold",
                        f"{base['name']} Supreme",
                    ],
                    "hybrids": [
                        f"{base['name']} Hybrid-1",
                        f"{base['name']} Hybrid-2",
                    ],
                    "region_specific_strains": [
                        f"{region} {base['name']} Local",
                    ],
                },
                "popular_varieties": [
                    f"{base['name']} Classic",
                    f"{base['name']} Hybrid-1",
                    f"{region} {base['name']} Local",
                ],
                "growth_cycle": {
                    "timeline": [
                        "Sowing: Day 0 - 15",
                        "Vegetative Stage: Day 16 - 45",
                        "Flowering Stage: Day 46 - 75",
                        "Maturity: Day 76 - 110",
                        "Harvesting: Day 111 - 145",
                    ],
                    "climate_requirements": f"{climate} climate with {season} season suitability.",
                },
                "timeline": [
                    "Sowing: Day 0 - 15",
                    "Vegetative Stage: Day 16 - 45",
                    "Flowering Stage: Day 46 - 75",
                    "Maturity: Day 76 - 110",
                    "Harvesting: Day 111 - 145",
                ],
                "soil_water_needs": {
                    "ideal_soil_type": soil,
                    "irrigation_methods": irrigation,
                    "rainfall_tolerance": rainfall,
                },
                "soil_water": f"{soil}; preferred method: {irrigation}; rainfall tolerance: {rainfall}.",
                "quick_facts": [
                    f"Growing Season: {season}",
                    f"Climate Requirement: {climate}",
                    f"Ideal Soil: {soil}",
                    f"Rainfall Tolerance: {rainfall}",
                ],
                "pests_diseases": f"Common issues in {base['name']} include blight, sucking pests, and stem borers depending on local conditions.",
                "nutrient_management": "Apply balanced NPK and micronutrients based on soil test for consistent yield.",
                "harvesting": f"Harvest when leaves turn yellow and moisture drops below 14%. Proper drying is crucial.",
            }
        )

    return records


def seed_crop_data() -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]

    records = _seed_records()
    operations = []
    valid_slugs = []
    for record in records:
        slug = record.get("slug") or _slugify(record["name"])
        record["slug"] = slug
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
    collection.create_index("name")
    collection.create_index("category")


def get_crops(category: Optional[str] = None, search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = get_db()
    collection = db[COLLECTION_NAME]

    query: Dict[str, Any] = {}
    if category:
        query["category"] = {"$regex": f"^{re.escape(category)}$", "$options": "i"}
    if search:
        query["$or"] = [
            {"name": {"$regex": re.escape(search), "$options": "i"}},
            {"scientific_name": {"$regex": re.escape(search), "$options": "i"}},
            {"category": {"$regex": re.escape(search), "$options": "i"}},
        ]

    cursor = collection.find(query).limit(limit)
    items: List[Dict[str, Any]] = []
    for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)

    return items


def get_crop_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    db = get_db()
    collection = db[COLLECTION_NAME]

    item = collection.find_one({"slug": slug})
    if not item:
        return None

    item["_id"] = str(item["_id"])
    return item
