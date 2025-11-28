import webbrowser
import json

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
def add_bookmark():
    choice = f"bookmarks{input('what set of bookmarks do you want to add a bookmark to? (1, 2, or 3)? ')}"
    new_bookmark = input("Enter the URL of the new bookmark: ")
    groups[choice].append(new_bookmark)
    with open('bookmarks.json', 'w') as json_file:
        json.dump(groups, json_file, indent=4)

def add_bookmark_loop():
    add_bookmark()
    while True:
        if input("Would you like to add another bookmark? (y/n): ").lower() == 'y':
            add_bookmark()
        else:
            print("Bookmarks updated.")
            break
        
def addsection():
    key=f"bookmarks{len(groups)+1}"
    groups[key]=[input("Enter the URL of the a bookmark: ")]
    with open('bookmarks.json', 'w') as json_file:
        json.dump(groups, json_file, indent=4)


def open_selection(select):
    for each in select:
        webbrowser.open(each)
    print("Good luck!")

def choose_bookmarks():
    choice = f"bookmarks{input('what set of bookmarks do you want to open? (1, 2, or 3)? ')}"
    open_selection(groups[choice])

