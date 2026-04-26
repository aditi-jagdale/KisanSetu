import random
from crop import get_db

base_diseases = [
    {
        "name": "Wheat Rust",
        "description": "A fungal disease that affects wheat stems and leaves, causing orange-red pustules.",
        "category": "Fungal",
        "prevalence": "Very Common",
        "symptoms": "Yellow, orange, or dark red pustules on the upper and lower leaf surfaces, stems, and sometimes the spike. These pustules burst, releasing powdery spores.",
        "control_methods": "Apply foliar fungicides such as Tebuconazole or Propiconazole at the first sign of infection. Ensure thorough coverage.",
        "preventive_measures": "Plant rust-resistant wheat varieties. Eliminate volunteer wheat and weed hosts that bridge the gap between crop cycles. Implement crop rotation.",
        "causal_agent": "Puccinia triticina (Fungus)",
        "spread": "Airborne spores carried by wind and rain splash.",
        "seasonality": "Cool, moist weather conditions in early spring.",
        "impact": "Can cause up to 30% yield loss if left untreated."
    },
    {
        "name": "Bacterial Blight",
        "description": "A severe bacterial infection causing water-soaked lesions that turn necrotic.",
        "category": "Bacterial",
        "prevalence": "Common",
        "symptoms": "Water-soaked streaks on leaves that turn brown or grayish-white. Lesions often ooze bacterial exudate in highly humid conditions.",
        "control_methods": "Apply copper-based bactericides early in the season. Chemical control is generally difficult once established.",
        "preventive_measures": "Use certified disease-free seeds. Avoid overhead irrigation to minimize leaf wetness. Practice deep plowing to bury crop residues.",
        "causal_agent": "Xanthomonas oryzae",
        "spread": "Irrigation water, rain splash, and contaminated tools.",
        "seasonality": "Hot, humid weather during monsoon or rainy seasons.",
        "impact": "Severe infections can lead to 60-75% yield reduction."
    },
    {
        "name": "Tomato Mosaic Virus",
        "description": "A viral disease causing mottling and discoloration of leaves, reducing fruit yield.",
        "category": "Viral",
        "prevalence": "Common",
        "symptoms": "Light and dark green mottled patterns on leaves. Leaves may become curled, malformed, or fern-like. Stunted plant growth and reduced fruit set.",
        "control_methods": "No chemical cure exists for viral infections. Remove and destroy infected plants immediately to prevent spread.",
        "preventive_measures": "Plant TMV-resistant tomato varieties. Disinfect tools frequently. Wash hands thoroughly with soap after handling plants.",
        "causal_agent": "Tomato Mosaic Virus (ToMV)",
        "spread": "Mechanical transmission through handling, tools, and grafting.",
        "seasonality": "Can occur year-round, especially prevalent in greenhouse settings.",
        "impact": "Reduces fruit quality and yield by up to 25%."
    },
    {
        "name": "Aphid Infestation",
        "description": "Small sap-sucking insects that stunt plant growth and transmit viral diseases.",
        "category": "Pest",
        "prevalence": "Very Common",
        "symptoms": "Curling, yellowing, and distorted leaves. Presence of sticky honeydew on lower leaves, which often leads to black sooty mold growth.",
        "control_methods": "Use insecticidal soaps, neem oil, or synthetic insecticides like Imidacloprid if the infestation is severe.",
        "preventive_measures": "Introduce natural predators like ladybugs or lacewings. Avoid over-fertilizing with nitrogen, which promotes lush growth that attracts aphids.",
        "causal_agent": "Aphididae family insects",
        "spread": "Winged adults fly to new host plants.",
        "seasonality": "Spring and early summer when plant growth is rapid.",
        "impact": "Stunts plant growth and acts as a major vector for destructive plant viruses."
    },
    {
        "name": "Nitrogen Deficiency",
        "description": "A nutrient disorder causing yellowing of older leaves and stunted plant growth.",
        "category": "Deficiencies",
        "prevalence": "Common",
        "symptoms": "General yellowing (chlorosis) that starts at the older, lower leaves and progresses upward. Plants appear stunted and pale overall.",
        "control_methods": "Apply fast-acting nitrogen fertilizers such as urea or ammonium nitrate directly to the soil or as a foliar spray.",
        "preventive_measures": "Conduct regular soil testing. Incorporate organic matter or compost before planting. Use appropriate fertilizer regimens based on crop needs.",
        "causal_agent": "Lack of available soil nitrogen",
        "spread": "Localized to areas with poor soil fertility or excessive leaching.",
        "seasonality": "Often appears after heavy rains (leaching) or during rapid growth phases.",
        "impact": "Significantly reduces vegetative growth, leading to low crop yields."
    },
    {
        "name": "Powdery Mildew",
        "description": "A fungal disease presenting as white, powdery spots on leaves and stems.",
        "category": "Fungal",
        "prevalence": "Very Common",
        "symptoms": "White or gray powdery spots on the upper surfaces of leaves, stems, and flowers. Over time, leaves turn yellow and drop prematurely.",
        "control_methods": "Apply sulfur-based fungicides or potassium bicarbonate sprays. Ensure thorough coverage of all plant parts.",
        "preventive_measures": "Ensure adequate spacing between plants to promote good air circulation. Avoid planting in heavily shaded areas.",
        "causal_agent": "Various species of the order Erysiphales",
        "spread": "Windborne spores.",
        "seasonality": "Warm, dry days with cool, humid nights (late summer to early autumn).",
        "impact": "Weakens plants and can severely reduce fruit yield and quality."
    },
    {
        "name": "Root Knot Nematodes",
        "description": "Microscopic roundworms that cause galls on roots, leading to poor nutrient uptake.",
        "category": "Pest",
        "prevalence": "Rare",
        "symptoms": "Above-ground symptoms include wilting during hot parts of the day, yellowing, and stunted growth. Roots exhibit distinct swollen galls or knots.",
        "control_methods": "Apply nematicides to the soil prior to planting. Solarize the soil during the hottest months to reduce nematode populations.",
        "preventive_measures": "Practice strict crop rotation with non-host crops like corn or marigolds. Use nematode-resistant plant varieties.",
        "causal_agent": "Meloidogyne species",
        "spread": "Movement of infested soil, water, or infected plant material.",
        "seasonality": "Most active in warm soils during summer months.",
        "impact": "Can cause complete crop failure in highly susceptible plants."
    },
    {
        "name": "Citrus Canker",
        "description": "A highly contagious bacterial disease causing lesions on citrus leaves, stems, and fruit.",
        "category": "Bacterial",
        "prevalence": "Rare",
        "symptoms": "Raised, corky, blister-like lesions on leaves, twigs, and fruit. Lesions are often surrounded by a yellow halo.",
        "control_methods": "Prune and burn infected plant parts. Spray copper-based bactericides repeatedly as a protective measure.",
        "preventive_measures": "Plant disease-free nursery stock. Implement strict sanitation measures for orchard equipment and personnel.",
        "causal_agent": "Xanthomonas axonopodis pv. citri",
        "spread": "Wind-driven rain, overhead irrigation, and contaminated tools.",
        "seasonality": "Warm, wet weather typical of tropical and subtropical regions.",
        "impact": "Leads to premature fruit drop, blemishes, and defoliation."
    },
    {
        "name": "Iron Chlorosis",
        "description": "A condition where leaves turn yellow while veins remain green, due to iron lack.",
        "category": "Deficiencies",
        "prevalence": "Common",
        "symptoms": "Interveinal chlorosis (yellowing between the green veins) on the youngest, newest leaves first. In severe cases, leaves may turn completely white.",
        "control_methods": "Apply chelated iron directly to the soil or as a foliar spray for rapid correction.",
        "preventive_measures": "Avoid overwatering. Lower the soil pH if it is highly alkaline, as high pH binds iron making it unavailable to plants.",
        "causal_agent": "High soil pH or compacted, waterlogged soils",
        "spread": "Localized to specific soil conditions.",
        "seasonality": "Often observed in early spring when soils are cool and wet.",
        "impact": "Reduces photosynthetic capacity, stunting growth and yield."
    },
    {
        "name": "Leaf Curl Virus",
        "description": "A viral infection transmitted by whiteflies causing severe upward curling of leaves.",
        "category": "Viral",
        "prevalence": "Very Common",
        "symptoms": "Severe upward or downward curling of leaves, vein clearing, stunted plant growth, and a drastic reduction in flower and fruit production.",
        "control_methods": "Infected plants cannot be cured and must be destroyed. Manage the vector population using yellow sticky traps and insecticides.",
        "preventive_measures": "Grow crops under insect-proof nets. Eradicate alternative weed hosts around the field.",
        "causal_agent": "Begomovirus (transmitted by Bemisia tabaci)",
        "spread": "Exclusively transmitted by the silverleaf whitefly.",
        "seasonality": "Peaks during warm, dry periods when whitefly populations surge.",
        "impact": "Can completely decimate susceptible crops like tomatoes and cotton."
    }
]

crops = ["Wheat", "Tomato", "Rice", "Cotton", "Sugarcane", "Potato", "Apple", "Banana", "Grape", "Onion"]
modifiers = ["Early", "Late", "Severe", "Mild", "Chronic", "Acute", "Regional", "Seasonal", "Widespread", "Isolated"]

diseases = []
diseases.extend(base_diseases)

for i in range(115):
    base = base_diseases[i % len(base_diseases)]
    crop = crops[i % len(crops)]
    mod = modifiers[i % len(modifiers)]
    
    new_disease = {
        "name": f"{mod} {crop} {base['name'].split()[-1]}",
        "description": f"A {mod.lower()} form of {base['name'].lower()} specifically affecting {crop.lower()} crops. {base['description']}",
        "category": base["category"],
        "prevalence": random.choice(["Very Common", "Common", "Rare"]),
        "symptoms": f"Observed specifically in {crop.lower()}: {base['symptoms']}",
        "control_methods": base["control_methods"],
        "preventive_measures": f"Specific to {crop.lower()} fields: {base['preventive_measures']}",
        "causal_agent": base["causal_agent"],
        "spread": base["spread"],
        "seasonality": base["seasonality"],
        "impact": base["impact"]
    }
    
    if any(d['name'] == new_disease['name'] for d in diseases):
        new_disease['name'] = f"{new_disease['name']} Type {i}"
        
    diseases.append(new_disease)

def seed_diseases():
    try:
        db = get_db()
        if db is not None:
            collection = db["diseases"]
            collection.drop() 
            collection.insert_many(diseases)
            print(f"Seeded {len(diseases)} detailed diseases into MongoDB.")
    except Exception as e:
        print("Error seeding diseases:", e)

def get_all_diseases():
    try:
        db = get_db()
        if db is not None:
            collection = db["diseases"]
            docs = list(collection.find({}, {"_id": 0}))
            if docs:
                return docs
    except Exception as e:
        print("Error fetching diseases:", e)
    return diseases