def formatEntry(homeTeam, awayTeam, date, time):
    return ["{} vs {}".format(homeTeam, awayTeam), date, time, date, time, "FALSE", "", ""]

from EuroFetcher.NetworkElement import *
import csv

with (
        NetworkElement(input("Flashscore link: ")) as ne,
        open('output.csv', mode='w', newline='') as file
    ):
    
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
              'All Day Event', 'Description', 'Location', 'Private']
    writer = csv.writer(file)
    writer.writerow(header)

    for match in ne.match_divs:
        writer.writerow(formatEntry(*match.match_data))