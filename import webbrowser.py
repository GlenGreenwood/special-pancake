import webbrowser
groups={"bookmarks1": ["https://docs.google.com/", "https://codecademy.com/","https://davinporter09.wixsite.com/shouldbelearning/"], "bookmarks2": ["https://www.khanacademy.com","https://classroom.google.com/","https://start.duckduckgo.com/"], "bookmarks3": ["https://www.coolmathgames.com/","https://www.example.com/","https://www.britannica.com/"]}

def open_selection(select):
    for each in select:
        webbrowser.open(each)
    print("Good luck!")

choice = "bookmarks"+ str(input("what set of bookmarks do you want to open? (1, 2, or 3)? "))
open=groups[choice]
open_selection(open)
