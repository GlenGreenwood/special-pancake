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

def backgroundImage(device_type):
    if type == 'Phone':
        bgImage = "Screenshot 2025-05-02 3.49.31 PM.png"
    else:
        bgImage = "Screenshot 2025-05-02 3.49.31 PM.png"
    return bgImage

def calculate_luminance(color):
    """Calculate the relative luminance of an RGB color."""
    r, g, b = [x / 255.0 for x in color]  # Normalize RGB values
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b  # Calculate luminance
    return luminance

def rgb_to_hex(rgb_colors):
    hex_colors = []
    for rgb in rgb_colors:
        # Ensure the RGB value is in the valid range
        if all(0 <= value <= 255 for value in rgb):
            hex_color = '{0:02X}{1:02X}{2:02X}'.format(rgb[0], rgb[1], rgb[2])
            hex_colors.append(hex_color)
        else:
            raise ValueError("RGB values must be between 0 and 255.")
    return hex_colors

def crembrule(device_type):
    bgImage = backgroundImage(device_type)
    color_thief = ColorThief(bgImage)
    palette=color_thief.get_palette(color_count=5)
    sorted_palette = sorted(palette, key=calculate_luminance)
    hex_codes=rgb_to_hex(sorted_palette)
    ddgBackgroundcolor = hex_codes[4]
    ddgTextcolor = hex_codes[3]
    ddgLinkcolor = hex_codes[2]
    ddgHeadercolor = hex_codes[1]
    ddgURLcolor = hex_codes[0]
    crembrule={
        "ddgBackgroundcolor": ddgBackgroundcolor,
        "ddgTextcolor": ddgTextcolor,
        "ddgLinkcolor": ddgLinkcolor,
        "ddgHeadercolor": ddgHeadercolor,
        "ddgURLcolor": ddgURLcolor
    }
    return crembrule



def SpirtualThought():
    pass

def waysToSayGL():
    pass
