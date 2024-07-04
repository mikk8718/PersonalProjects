from TwitchNetworkElement import *
import subprocess 
    
with (
        TwitchNetworkElement("https://www.twitch.tv/directory/category/league-of-legends", 
                             SearchType.LOW_TO_HIGH) as twe,
        Menu(twe.streamers.format, "TwitchFetcher", twe) as menu
    ):
    
    with subprocess.Popen(["streamlink", menu.target_streamer, "best"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdout, stderr = p.communicate()
        
    