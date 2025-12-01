import book as book
from flask import Flask, request, redirect, render_template, jsonify, session, make_response
import json
import webbrowser
from colorthief import ColorThief
import requests
import re
import random
from datetime import datetime, timedelta
import codecs
from urllib.parse import quote
import os
import uuid
from cryptography.fernet import Fernet  # NEW: for encryption

def rot13(text):
    return codecs.encode(text, 'rot_13')

app = Flask(__name__)

# ------------------ Encryption Setup ------------------
# Use a single key for all devices (or generate one per device if needed)
KEY_FILE = "secret.key"
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        ENCRYPTION_KEY = f.read()
else:
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(ENCRYPTION_KEY)
fernet = Fernet(ENCRYPTION_KEY)
# --------------------------------------------------------

# ------------------ Device Identification ------------------
@app.before_request
def identify_device():
    device_id = request.cookies.get("device_id")
    if not device_id:
        # Generate a new device ID
        device_id = str(uuid.uuid4())
        resp = make_response()
        resp.set_cookie("device_id", device_id, max_age=10*365*24*60*60)  # 10 years
        request.device_id = device_id
        return resp
    request.device_id = device_id
# --------------------------------------------------------

app.secret_key = os.urandom(24)

# Placeholder setup
darkmode = False
pressed = False
try:
    with open("placeholder.json", "r") as f:
        placeholderlist = json.load(f)
except FileNotFoundError:
    placeholderlist = []
funPlaceholder = random.choice(list(placeholderlist)) if placeholderlist else "Search..."

groups = book.load_groups()

# ------------------ Utility Functions ------------------
def encrypt_data(data: dict) -> bytes:
    """Encrypt a Python dict and return bytes."""
    json_data = json.dumps(data).encode('utf-8')
    return fernet.encrypt(json_data)

def decrypt_data(data: bytes) -> dict:
    """Decrypt bytes to a Python dict."""
    json_data = fernet.decrypt(data).decode('utf-8')
    return json.loads(json_data)
# --------------------------------------------------------

@app.route('/')
def home():
    thought = request.args.get("thought")
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    fact = "Fun Fact: "+data["text"]
    try:
        with open("placeholder.json", "r") as f:
            placeholderlist = json.load(f)
    except FileNotFoundError:
        placeholderlist = [fact]*6 + ["This is a placeholder for a function I will add later."]
    funPlaceholder = random.choice(list(placeholderlist)) if placeholderlist else "Search..."
    device_type = book.deviceType()
    pressed = session.get('pressed', False)
    bgImage = book.backgroundImage(device_type, darkmode, pressed)
    backgroundImage = bgImage
    engine_crembrule = book.engine_crembrule(device_type, darkmode, backgroundImage)
    css_crembrule = book.css_crembrule(device_type, darkmode, backgroundImage)
    return render_template('index.html', **engine_crembrule, **css_crembrule, funPlaceholder=funPlaceholder, backgroundImage=bgImage, fact=fact, thought=thought)
    

@app.route('/set-theme', methods=['POST'])
def set_theme():
    global darkmode
    selected_theme = request.form.get('theme')
    session['pressed'] = False
    darkmode = (selected_theme == 'dark')
    return redirect('/')

@app.route('/form')
def form():
    return "<form action='/submit' method='POST'><button type='submit' name='my_button'>Press Me!</button></form>"

@app.route('/form/submit', methods=['POST'])
def submit():
    book.add_bookmark_loop()
    return "Bookmarks updated. You can close this tab."


# ------------------ Per-device encrypted search history ------------------
def get_history_filename():
    device_id = getattr(request, 'device_id', None)
    return f"search_history_{device_id}.json.enc" if device_id else None

@app.route("/update-history", methods=["POST"])
def update_history():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"status": "empty"}), 400

    filename = get_history_filename()
    if filename and os.path.exists(filename):
        with open(filename, "rb") as f:
            try:
                history = decrypt_data(f.read())
            except:
                history = {}
    else:
        history = {}

    history[query] = {"last_used": datetime.utcnow().isoformat()}

    with open(filename, "wb") as f:
        f.write(encrypt_data(history))

    return jsonify({"status": "ok"})

def load_search_history(max_age_days=10):
    filename = get_history_filename()
    if not filename or not os.path.exists(filename):
        return []

    try:
        with open(filename, "rb") as f:
            history = decrypt_data(f.read())
    except:
        history = {}

    now = datetime.utcnow()
    filtered = []
    for query, info in history.items():
        last_used = datetime.fromisoformat(info["last_used"])
        if now - last_used <= timedelta(days=max_age_days):
            filtered.append(query + "⏳")
    return filtered
# --------------------------------------------------------

def load_bookmarks():
    with open("bookmarks.json") as f:
        data = json.load(f)
    bookmark_list = []
    for group in data.values():
        for url in group:
            bookmark_list.append(f"{url} 🔖".replace("https://","").replace("http://","").replace("www.",""))
    return bookmark_list

def load_static_suggestions():
    try:
        with open("suggestions.json") as f:
            suggestions = json.load(f)
    except FileNotFoundError:
        suggestions = []
    return suggestions

@app.route("/suggestions")
def suggestions():
    query = request.args.get("q", "").lower()
    bookmarks = load_bookmarks()
    history = load_search_history()
    suggestions = load_static_suggestions()
    combined = bookmarks + suggestions + history

    # fun fact
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    fact = ["Fun Fact: "+data["text"]]

    filtered = [s for s in combined if query in s.lower()]

    if query:
        filtered += fact + [rot13(query)]
    
    secret_key = "wizard squirrel"
    secret_message = "🎉 Click here for surprise!"
    if secret_key in query:
        filtered.append(secret_message)

    return jsonify(filtered)


@app.route('/spiritual-thought', methods=['GET','POST'])
def spiritual_thought_button():
    device_type = book.deviceType()
    session['pressed'] = True
    thought = book.SpirtualThought(device_type, darkmode)
    return redirect(f"/?thought={quote(thought)}")

if __name__ == '__main__':
    app.run(debug=True)
