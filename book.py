import webbrowser
import json
from flask import Flask, request, redirect
from colorthief import ColorThief
from user_agents import parse
import random

# Establishing default bookmark groups and loading any existing bookmarks from a JSON file
def load_groups():
    groups={"bookmarks1": ["https://docs.google.com/", "https://codecademy.com/","https://davinporter09.wixsite.com/shouldbelearning/"], "bookmarks2": ["https://www.khanacademy.com","https://classroom.google.com/","https://start.duckduckgo.com/"], "bookmarks3": ["https://www.coolmathgames.com/","https://www.example.com/","https://www.britannica.com/"]}
    try:
        with open('bookmarks.json', 'r') as json_file:
            groups.update(json.load(json_file))
    except:
        pass
    return groups

groups=load_groups()

#defines the function that adds a bookmark to the one of the selected sections. This funtion is called in many others.
def add_bookmark(section, url):
    choice = f"bookmarks{str(section)}"
    groups[choice].append(url)
    with open('bookmarks.json', 'w') as json_file:
        json.dump(groups, json_file, indent=4)

#This doesn't work because I would need to pass the parameters multiple times while the function is running.
#def add_bookmark_loop(section, url):
#    add_bookmark(section, url)
#    while True:
#        if input("Would you like to add another bookmark? (y/n): ").lower() == 'y':
#            add_bookmark()
#        else:
#            return "bookmarks updated"
#            break
        
def addsection():
    key=f"bookmarks{len(groups)+1}"
    groups[key]=[input("Enter the URL of the a bookmark: ")]
    with open('bookmarks.json', 'w') as json_file:
        json.dump(groups, json_file, indent=4)


def open_selection(select):
    for each in select:
        webbrowser.open(each)
    print("Good luck!")

#this still has to be called from the console. I need to make a form for it.
def choose_bookmarks():
    choice = f"bookmarks{input('what set of bookmarks do you want to open? (1, 2, or 3)? ')}"
    open_selection(groups[choice])

def deviceType():
    user_agent = request.headers.get('User-Agent')
    parsed = parse(user_agent)
    
    if parsed.is_mobile:
        device_type = 'Phone'
    else:
        device_type = 'Desktop'
    return device_type

def backgroundImage():
    type=deviceType()
    if type == 'Phone':
        bgImage = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pixelstalk.net%2Fwp-content%2Fuploads%2F2016%2F07%2FDownload-Free-Pictures-3840x2160.jpg&f=1&nofb=1&ipt=832199581a53e02994f6809a03e36af683a87209e0e0a4ab3e9efad84a270390"
    else:
        bgImage = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pixelstalk.net%2Fwp-content%2Fuploads%2F2016%2F07%2FDownload-Free-Pictures-3840x2160.jpg&f=1&nofb=1&ipt=832199581a53e02994f6809a03e36af683a87209e0e0a4ab3e9efad84a270390"
    return bgImage

def colors():
    bgImage = backgroundImage()
    color_thief = ColorThief(bgImage)
    colors=color_thief.get_palette(color_count=6)
    ddgBackgroundcolor = "placeholder"
    ddgTextcolor = "placeholder"
    ddgLinkcolor = "placeholder"
    ddgHeadercolor = "placeholder"
    ddgURLcolor = "placeholder"
    return colors
print(colors())
def SpirtualThought():
    pass

def waysToSayGL():
    pass
