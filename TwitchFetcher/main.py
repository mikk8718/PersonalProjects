from TwitchNetworkElement import *
import subprocess 
    
with (
        TwitchNetworkElement("https://www.twitch.tv/directory/category/league-of-legends", 
                             SearchType.HIGH_TO_LOW) as twe,
        Menu(twe.streamers.formated, "TwitchFetcher", twe) as menu
    ):
    
    with subprocess.Popen(["streamlink", menu.target_streamer, "best"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdout, stderr = p.communicate()
        
    