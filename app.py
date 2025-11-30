import book as book
from flask import Flask, request, redirect, render_template, jsonify
import json
import webbrowser
from colorthief import ColorThief
import requests
import re
import random
from datetime import datetime, timedelta
import codecs
from urllib.parse import quote

def rot13(text):
    return codecs.encode(text, 'rot_13')

app = Flask(__name__)


#this sets up the variable for later, but I need to figure out how to make it persist between sessions.
darkmode = False
pressed = False
try:
    with open("placeholder.json", "r") as f:
        placeholderlist = json.load(f)
except FileNotFoundError:
    placeholderlist = []
funPlaceholder = random.choice(list(placeholderlist)) if placeholderlist else "Search..."

groups = book.load_groups()





#I am working on the rest of the new tab page before I circle back to bookmarks.
@app.route('/')
def home():
    #get the spiritual thought if requested.
    thought = request.args.get("thought")
    #this gets a random fun fact from an API to use as a placeholder in the search bar.
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    fact = "Fun Fact: "+data["text"]
    #This picks a random fact from the APT if the JSON is down or unreachable.
    try:
        with open("placeholder.json", "r") as f:
            placeholderlist = json.load(f)
    except FileNotFoundError:
        placeholderlist = [fact, fact, fact, fact, fact, fact, "This is a placeholder for a function I will add later."]
    funPlaceholder = random.choice(list(placeholderlist)) if placeholderlist else "Search..."
    device_type = book.deviceType()
    bgImage=book.backgroundImage(device_type, darkmode, pressed)
    backgroundImage=bgImage    #f"{bgImage}?v={int(time())}" #f"/workspaces/special-pancake/static/{}"
    engine_crembrule=book.engine_crembrule(device_type, darkmode, backgroundImage)
    css_crembrule=book.css_crembrule(device_type, darkmode, backgroundImage)
    return render_template('index.html', **engine_crembrule, **css_crembrule, funPlaceholder=funPlaceholder, backgroundImage=bgImage, fact=fact, thought=thought)
    

@app.route('/set-theme', methods=['POST'])
def set_theme():
    global darkmode
    selected_theme = request.form.get('theme')
    if selected_theme == 'dark':
        darkmode = True
    else:
        darkmode = False
    return redirect('/')

#this current version only lets you add bookmarks with the console. I need to add a form on a seperate page (or a pop-up of some kind) that will take all of the input parameters that the input functions ask for.
@app.route('/form')
def form():
    return   "<form action='/submit' method='POST'><button type='submit' name='my_button'>Press Me!</button></form>"



#this is exactly what AI wrote. I will need to modify it to fit my needs later.
@app.route('/form/submit', methods=['POST'])
def submit():
    book.add_bookmark_loop()
    return "Bookmarks updated. You can close this tab."
#This is great unless it saves a fun fact, or it keeps unneccesary history items. Also, not great for privacy or efficiency.
@app.route("/update-history", methods=["POST"])
def update_history():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"status": "empty"}), 400
    
    try:
        with open("search_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}

    # Update last_used timestamp
    history[query] = {"last_used": datetime.utcnow().isoformat()}

    with open("search_history.json", "w") as f:
        json.dump(history, f, indent=4)

    return jsonify({"status": "ok"})

def load_bookmarks():
    with open("bookmarks.json") as f:
        data = json.load(f)
    bookmark_list = []
    for group in data.values():
        for url in group:
            bookmark_list.append(f"{url} 🔖".replace("https://","").replace("http://","").replace("www.",""))
    return bookmark_list

def load_search_history(max_age_days=10):
    try:
        with open("search_history.json") as f:
            history = json.load(f)
    except FileNotFoundError:
        return []

    # Filter out unused/old searches
    now = datetime.now()
    filtered = []
    for query, info in history.items():
        last_used = datetime.fromisoformat(info["last_used"])
        if now - last_used <= timedelta(days=max_age_days):
            filtered.append(query + "⏳")
    return filtered

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

    # Filter suggestions based on what user typed
    filtered = [s for s in combined if query in s.lower()]

    if query:
        filtered = filtered + fact + [rot13(query)]

    return jsonify(filtered)


@app.route('/spiritual-thought', methods=['GET','POST'])
def spiritual_thought_button():
    device_type = book.deviceType()
    thought = book.SpirtualThought(device_type, darkmode)
    # urlencode the thought so it’s safe in the URL
    return redirect(f"/?thought={quote(thought)}")

if __name__ == '__main__':
    app.run(debug=True)
