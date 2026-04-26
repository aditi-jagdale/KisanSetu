import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ✅ ONLY crop-related imports
from crop import get_crop_by_slug, get_crops, get_db, seed_crop_data

load_dotenv()

app = Flask(__name__)

# Secret Key
app.secret_key = os.getenv("SECRET_KEY") or "supersecretkey123"

# MongoDB Setup
try:
    db = get_db()
    users_collection = db["users"]
    seed_crop_data()
    print("MongoDB connected successfully")
except Exception as e:
    print("MongoDB connection failed:", e)
    users_collection = None


# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    user = session.get('user')
    name = session.get('name')

    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])

    return render_template('index.html', user=user, initial=initial)


# ---------- AUTH ---------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if users_collection is None:
            return "Database not connected ❌"

        user = users_collection.find_one({
            "email": email,
            "password": password
        })

        if user:
            session['user'] = email
            session['name'] = user['name']
            return redirect(url_for('index'))
        else:
            return "Invalid credentials ❌"

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if users_collection is None:
            return "Database not connected ❌"

        if users_collection.find_one({"email": email}):
            return "User already exists ⚠️"

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return redirect(url_for('login'))

    return render_template('signup.html')


# ---------- CROP PAGE ---------- #

@app.route('/crop')
def crop():
    if 'user' not in session:
        return redirect(url_for('login'))

    name = session.get('name')
    initial = ""

    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words[:2]])

    return render_template(
        'crop.html',
        user=session.get('user'),
        initial=initial
    )


@app.route('/api/crops')
def api_crops():
    category = request.args.get('category')
    search = request.args.get('search')

    data = get_crops(category=category, search=search, limit=600)

    return jsonify({"ok": True, "crops": data})


@app.route('/api/crops/<slug>')
def api_crop_detail(slug):
    crop_item = get_crop_by_slug(slug)

    if not crop_item:
        return jsonify({"ok": False, "message": "Crop not found"}), 404

    return jsonify({"ok": True, "crop": crop_item})

from disease import seed_diseases, get_all_diseases
from market import seed_market_data, get_market_prices
from fertilizer import seed_fertilizer_data, get_fertilizers
from farming import seed_farming_data, get_all_techniques

seed_diseases()
seed_market_data()
seed_fertilizer_data()
seed_farming_data()

# ---------- FERTILIZER PAGE ---------- #

@app.route('/fertilizer')
def fertilizer():
    user = session.get('user')
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])
    return render_template('fertilizer.html', user=user, initial=initial)

@app.route('/api/fertilizers')
def api_fertilizers():
    f_type = request.args.get('type')
    nutrient = request.args.get('nutrient')
    form = request.args.get('form')
    brand = request.args.get('brand')
    
    data = get_fertilizers(f_type=f_type, nutrient=nutrient, form=form, brand=brand)
    return jsonify(data)

# ---------- MARKET PAGE ---------- #

@app.route('/market')
def market():
    user = session.get('user')
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])
    return render_template('market.html', user=user, initial=initial)

@app.route('/api/market')
def api_market():
    crop = request.args.get('crop')
    state = request.args.get('state')
    market = request.args.get('market')
    
    data = get_market_prices(crop=crop, state=state, market=market)
    return jsonify(data)

@app.route('/disease')
def disease():
    user = session.get('user')
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])
    return render_template('disease.html', user=user, initial=initial)

# ---------- SCHEME PAGE ---------- #

@app.route('/scheme')
def scheme():
    user = session.get('user')
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])
    return render_template('scheme.html', user=user, initial=initial)

@app.route('/farming')
def farming():
    user = session.get('user')
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words])
    techniques = get_all_techniques()
    return render_template('farming.html', user=user, initial=initial, techniques=techniques)

@app.route('/api/diseases')
def api_diseases():
    return jsonify(get_all_diseases())



# ---------- LOGOUT ---------- #

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)