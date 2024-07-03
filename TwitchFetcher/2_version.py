from TwitchFetcher.TwitchNetworkElement import *
from simple_term_menu import TerminalMenu
import subprocess 

with TwitchNetworkElement("https://www.twitch.tv/directory/category/league-of-legends", 
                        SearchType.LOW_TO_HIGH,
                        ) as twe:
        
    url_base = "https://twitch.tv/"

    streamer_menu = TerminalMenu(twe.streamers.format, title="Streams")
    
    stream_menu_index = streamer_menu.show()

    if(stream_menu_index == 0):
        search = url_base+input("Streamer name: ")
        
    with subprocess.Popen(["streamlink", url_base + twe.streamers[stream_menu_index].handle, "best"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdout, stderr = p.communicate()
        