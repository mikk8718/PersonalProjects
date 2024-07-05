from NetworkElement import *
import webbrowser

with (
        NetworkElement("https://www.flashscore.dk/nyheder/fodbold") as ne,
        Menu(ne.articles.titles, "{} New Articles".format(len(ne.articles))) as menu
    ):    
    try:
        for i in menu.index: webbrowser.open_new_tab(ne.articles[i].link)
    except:
        raise Exception("error")
    
