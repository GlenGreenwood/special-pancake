import book
from flask import Flask
import json
import webbrowser
app = Flask(__name__)

groups = book.load_groups()
#this current version only lets you add bookmarks with the console. I need to add a form on a seperate page (or a pop-up of some kind) that will take all of the input parameters that the input functions ask for.
@app.route('/')
def index():
    return   "<form action='/submit' method='POST'><button type='submit' name='my_button'>Press Me!</button></form>"
@app.route('/submit', methods=['POST'])
def submit():
    book.add_bookmark_loop()
    return "Bookmarks updated. You can close this tab."

if __name__ == '__main__':
    app.run(debug=True)
