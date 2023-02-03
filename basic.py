import os
import re
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import json

songs = {}

sumListen = 0
numSongs = 0
averagePlay = 0


def main():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    # show an "Open" dialog box and return the path to the selected file
    # directory = askdirectory()

    # files = getFiles(directory)

    # for f in files:
    #     calculateFile(f)

    file = askopenfilename()

    calculateFile(file)

    averageListen = calculateAverageTimePlayed()
    sortedSongs = sortSongs()

    for song in sortedSongs[:10]:
        print(song)


def getFiles(directory):

    files = []

    for f in os.listdir(directory):
        if re.match(r'endsong', f):
            files.append(os.path.join(directory, f))

    return files


def calculateFile(filename):
    f = open(filename)
    data = json.load(f)

    for song in data:
        if song['ms_played'] > 0:
            timePlayed(song)
            playedSongs(song)


def playedSongs(song):
    global songs

    name = song['master_metadata_track_name']
    if name not in songs:
        songs[name] = {
            "timePlayed": song['ms_played'],
            "numPlays": 1
        }
    else:
        songs[name]["timePlayed"] += song['ms_played']
        songs[name]["numPlays"] += 1


def sortSongs():

    global songs

    return [(k, songs[k]) for k in sorted(songs.items(), key=lambda d: d[1]['numPlays'], reverse=True)]


def timePlayed(song):
    global sumListen
    global numSongs

    sumListen += int(song['ms_played'])/1000
    numSongs += 1


def calculateAverageTimePlayed():
    return sumListen / numSongs


if __name__ == "__main__":
    main()
