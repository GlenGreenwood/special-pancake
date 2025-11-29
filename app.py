import book as book
from flask import Flask, request, redirect, render_template
import json
import webbrowser
from colorthief import ColorThief
app = Flask(__name__)

#this will be used later to toggle dark mode on and off.
darkmode = True
funPlaceholder = "This is a placeholder for a function I will add later."
groups = book.load_groups()
#I am working on the rest of the new tab page before I circle back to bookmarks.
@app.route('/')
def home():
    device_type = book.deviceType()
    bgImage=book.backgroundImage(device_type, darkmode)
    backgroundImage=f"/workspaces/special-pancake/static/{bgImage}"
    engine_crembrule=book.engine_crembrule(device_type, darkmode, backgroundImage)
    css_crembrule=book.css_crembrule(device_type, darkmode, backgroundImage)
    return render_template('index.html', **engine_crembrule, **css_crembrule, funPlaceholder=funPlaceholder, backgroundImage=bgImage)
    



#this current version only lets you add bookmarks with the console. I need to add a form on a seperate page (or a pop-up of some kind) that will take all of the input parameters that the input functions ask for.
@app.route('/form')
def form():
    return   "<form action='/submit' method='POST'><button type='submit' name='my_button'>Press Me!</button></form>"
@app.route('/form/submit', methods=['POST'])
def submit():
    book.add_bookmark_loop()
    return "Bookmarks updated. You can close this tab."

if __name__ == '__main__':
    app.run(debug=True)
