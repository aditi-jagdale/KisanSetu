import os
import re

template_dir = r"c:\Users\Sri Maruti\OneDrive\Desktop\WEBSITE\templates"

nav_template = """      <nav class="main-nav">
        <a {home_act} href="{{{{ url_for('index') }}}}">Home</a>
        <a {crop_act} href="{{{{ url_for('crop') }}}}">Crops</a>
        <a {farming_act} href="{{{{ url_for('farming') }}}}">Farming Techniques</a>
        <a {market_act} href="{{{{ url_for('market') }}}}">Market Prices</a>
        <a {disease_act} href="{{{{ url_for('disease') }}}}">Disease Directory</a>
        <a {fert_act} href="{{{{ url_for('fertilizer') }}}}">Fertilizers</a>
        <a {scheme_act} href="{{{{ url_for('scheme') }}}}">Schemes</a>
      </nav>"""

files = {
    "index.html": "home",
    "crop.html": "crop",
    "farming.html": "farming",
    "market.html": "market",
    "disease.html": "disease",
    "fertilizer.html": "fert",
    "scheme.html": "scheme"
}

for filename, active_key in files.items():
    filepath = os.path.join(template_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate the nav specific to this file
    kwargs = {k: "" for k in ["home_act", "crop_act", "farming_act", "market_act", "disease_act", "fert_act", "scheme_act"]}
    kwargs[f"{active_key}_act"] = 'class="active"'
    
    new_nav = nav_template.format(**kwargs)

    # Regex to find <nav class="main-nav">...</nav>
    pattern = re.compile(r'<nav class="main-nav">.*?</nav>', re.DOTALL)
    
    # Check if there is a match
    if pattern.search(content):
        # We need to preserve the leading whitespace of the matched nav
        match = pattern.search(content)
        
        # Replace
        new_content = pattern.sub(new_nav, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"Nav not found in {filename}")
