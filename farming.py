from crop import get_db

base_techniques = [
    {
        "name": "Crop Rotation",
        "description": "Growing different types of crops in the same area across a sequence of seasons.",
        "benefits": "Improves soil health, reduces pests, and prevents soil depletion.",
        "category": "Organic",
        "difficulty": "Easy",
        "estimated_cost": "Low",
        "water_usage": "Medium",
        "suitable_crops": ["Wheat", "Corn", "Soybeans"],
        "icon": "fa-arrows-rotate"
    },
    {
        "name": "Precision Agriculture",
        "description": "Using technology like GPS and sensors to optimize field-level management.",
        "benefits": "Increases yield, reduces waste, and lowers environmental impact.",
        "category": "Modern",
        "difficulty": "Hard",
        "estimated_cost": "High",
        "water_usage": "Low",
        "suitable_crops": ["Corn", "Cotton", "Wheat"],
        "icon": "fa-satellite-dish"
    },
    {
        "name": "Drip Irrigation",
        "description": "Delivering water directly to the roots of plants through a network of valves, pipes, and tubing.",
        "benefits": "Saves water, reduces weed growth, and improves crop quality.",
        "category": "Irrigation",
        "difficulty": "Medium",
        "estimated_cost": "Medium",
        "water_usage": "Low",
        "suitable_crops": ["Tomatoes", "Peppers", "Strawberries"],
        "icon": "fa-droplet"
    },
    {
        "name": "Cover Cropping",
        "description": "Planting crops primarily to manage soil erosion, soil quality, water, weeds, and pests.",
        "benefits": "Enhances soil structure, adds organic matter, and fixes nitrogen.",
        "category": "Soil Management",
        "difficulty": "Easy",
        "estimated_cost": "Low",
        "water_usage": "Low",
        "suitable_crops": ["Legumes", "Radishes", "Oats"],
        "icon": "fa-seedling"
    },
    {
        "name": "Hydroponics",
        "description": "Growing plants without soil by using mineral nutrient solutions in an aqueous solvent.",
        "benefits": "Requires less water, allows year-round growth, and maximizes space.",
        "category": "Modern",
        "difficulty": "Hard",
        "estimated_cost": "High",
        "water_usage": "Low",
        "suitable_crops": ["Lettuce", "Spinach", "Herbs"],
        "icon": "fa-water"
    },
    {
        "name": "Agroforestry",
        "description": "Integrating trees and shrubs into crop and animal farming systems.",
        "benefits": "Increases biodiversity, improves soil structure, and diversifies income.",
        "category": "Sustainable",
        "difficulty": "Medium",
        "estimated_cost": "Medium",
        "water_usage": "Medium",
        "suitable_crops": ["Coffee", "Cocoa", "Fruit Trees"],
        "icon": "fa-tree"
    },
    {
        "name": "No-Till Farming",
        "description": "Growing crops or pasture without disturbing the soil through tillage.",
        "benefits": "Prevents soil erosion, retains moisture, and reduces labor costs.",
        "category": "Soil Management",
        "difficulty": "Medium",
        "estimated_cost": "Low",
        "water_usage": "Low",
        "suitable_crops": ["Corn", "Soybeans", "Wheat"],
        "icon": "fa-tractor"
    },
    {
        "name": "Integrated Pest Management (IPM)",
        "description": "An eco-friendly approach to managing pests using biological, cultural, and chemical tools.",
        "benefits": "Minimizes pesticide use, protects beneficial insects, and is cost-effective.",
        "category": "Organic",
        "difficulty": "Medium",
        "estimated_cost": "Medium",
        "water_usage": "Medium",
        "suitable_crops": ["Apples", "Grapes", "Tomatoes"],
        "icon": "fa-bug-slash"
    },
    {
        "name": "Terracing",
        "description": "Creating stepped levels on hilly or mountainous terrain to cultivate crops.",
        "benefits": "Reduces soil erosion, manages water runoff, and makes steep land arable.",
        "category": "Traditional",
        "difficulty": "Hard",
        "estimated_cost": "High",
        "water_usage": "Medium",
        "suitable_crops": ["Rice", "Tea", "Potatoes"],
        "icon": "fa-layer-group"
    },
    {
        "name": "Composting",
        "description": "Decaying organic material to use as a natural fertilizer for crops.",
        "benefits": "Reduces waste, enriches soil, and decreases the need for chemical fertilizers.",
        "category": "Organic",
        "difficulty": "Easy",
        "estimated_cost": "Low",
        "water_usage": "Low",
        "suitable_crops": ["Vegetables", "Flowers", "Herbs"],
        "icon": "fa-recycle"
    }
]

adjectives = ["Advanced", "Automated", "Smart", "Eco-friendly", "High-yield", "Traditional", "Sustainable", "Intensive", "Adaptive", "Climate-resilient"]

techniques = []
techniques.extend(base_techniques)

for i in range(90):
    base = base_techniques[i % len(base_techniques)]
    adjective = adjectives[i % len(adjectives)]
    
    new_technique = {
        "name": f"{adjective} {base['name']}",
        "description": f"An enhanced implementation of {base['name'].lower()} focusing on {adjective.lower()} methods.",
        "benefits": f"{base['benefits']} Additionally optimized for modern farming needs.",
        "category": base["category"],
        "difficulty": base["difficulty"],
        "estimated_cost": base["estimated_cost"],
        "water_usage": base["water_usage"],
        "suitable_crops": base["suitable_crops"],
        "icon": base["icon"]
    }
    techniques.append(new_technique)

def seed_farming_data():
    try:
        db = get_db()
        if db is not None:
            collection = db["farming_techniques"]
            collection.drop() # Drop to re-seed with detailed schema
            collection.insert_many(techniques)
            print("Seeded 100 detailed farming techniques into MongoDB.")
    except Exception as e:
        print("Error seeding farming techniques:", e)

def get_all_techniques():
    try:
        db = get_db()
        if db is not None:
            collection = db["farming_techniques"]
            docs = list(collection.find({}, {"_id": 0}))
            if docs:
                return docs
    except Exception as e:
        print("Error fetching farming techniques:", e)
    return techniques
