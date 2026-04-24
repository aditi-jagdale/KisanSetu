import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from crop import get_crop_by_slug, get_crops, get_db, seed_crop_data
from farming import seed_farming_data, get_techniques

load_dotenv()

app = Flask(__name__)

# ✅ Secret Key Fix
app.secret_key = os.getenv("SECRET_KEY") or "supersecretkey123"

try:
    db = get_db()
    users_collection = db["users"]
    seed_crop_data()
    seed_farming_data()
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


@app.route('/crop')
def crop():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words[:2]])
    return render_template('crop.html', user=session.get('user'), initial=initial)


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


@app.route('/farming')
def farming():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = session.get('name')
    initial = ""
    if name:
        words = name.split()
        initial = "".join([w[0].upper() for w in words[:2]])
    return render_template('farming.html', user=session.get('user'), initial=initial)


@app.route('/api/farming')
def api_farming():
    data = get_techniques()
    return jsonify({"ok": True, "techniques": data})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)