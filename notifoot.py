"""
Notifoot: follow your favorite matches while working!
"""

from plyer import notification
import json
import requests
import time
from datetime import datetime as dt

# Constants
periodRefresh = 15
notifRefresh = 300
timeZone_sec = 3600

# Useful variables (will be refreshed)
scoreHome = []
scoreAway = []
dateOfStart = []
lastNotif = 0


def periodicNotif():
    messages = ""
    for i in range(len(timeMatch)):
        if (timeMatch[i] is None):
            messages = messages + str(teamHome[i]) + " vs " + str(
                teamAway[i]) + " will start @ " + str(dateOfStart[i])[11:16] + " UTC\n"
        elif (timeMatch[i] == "full-time"):
            messages = messages + "Final score: " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"
        else:
            messages = messages + "@ t = " + str(timeMatch[i]) + " : " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"
    notification.notify(
        title="Match statuses:",
        # Sample msg: "@ t = 15': AAA 0 - 2 BBB"
        message=messages,
        timeout=5
    )


def printScores():
    messages = ""
    for i in range(len(timeMatch)):
        if (timeMatch[i] is None):
            messages = messages + str(teamHome[i]) + " vs " + str(
                teamAway[i]) + " will start @ " + str(dateOfStart[i])[11:16] + " UTC\n"
        elif (timeMatch[i] == "full-time"):
            messages = messages + "Final score: " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"
        else:
            messages = messages + "@ t = " + str(timeMatch[i]) + " : " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"
    print(messages)


def goalNotif():
    messages = ""
    for i in range(len(timeMatch)):
        if (timeMatch[i] is None):
            messages = messages + str(teamHome[i]) + " vs " + str(
                teamAway[i]) + " will start @ " + str(dateOfStart[i])[11:16] + " UTC\n"
        elif (timeMatch[i] == "full-time"):
            messages = messages + "Final score: " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"
        else:
            messages = messages + "@ t = " + str(timeMatch[i]) + " : " + str(teamHome[i]) + " " + \
                str(scoreHome[i]) + " - " + \
                str(scoreAway[i]) + " " + str(teamAway[i]) + "\n"

    notification.notify(
        title="⚽ GOAAAAL!!!",
        # Sample msg: "@ t = 15': AAA 0 - 2 BBB"
        message=messages,
        timeout=40
    )


def refreshScore():
    apiUrl = "https://worldcupjson.net/matches/today?by_date=asc"
    urlDump = requests.get(apiUrl).text
    jsonData = json.loads(urlDump)
    # print(jsonData)
    nbMatches = len(jsonData)
    print("There are", str(len(jsonData)), "matches today!")

    for i in range(nbMatches):
        teamHome.append(jsonData[i]['home_team']['country'])
        teamAway.append(jsonData[i]['away_team']['country'])
        scoreHome.append(jsonData[i]['home_team']['goals'])
        scoreAway.append(jsonData[i]['away_team']['goals'])
        timeMatch.append(jsonData[i]['time'])
        dateOfStart.append(jsonData[i]['datetime'])


while (True):
    timeMatch = []
    teamHome = []
    teamAway = []
    dateOfStart = []
    oldScoreHome = scoreHome
    oldScoreAway = scoreAway
    refreshScore()
    dateOfStartEpoch = [dt.strptime(
        date, "%Y-%m-%dT%H:%M:%SZ").timestamp() for date in dateOfStart]
    printScores()
    # Do not do anything until start of match
    if (len(dateOfStartEpoch) == 0):
        print("No matches today. You can fully focus on your work!")
        time.sleep(7200)
    elif ((time.time() - 120) < (min(dateOfStartEpoch) + timeZone_sec)):
        timeToSleep = min(dateOfStartEpoch) - time.time() + timeZone_sec - 120
        print("First match starts at", str(min(dateOfStart)))
        print("Next match in", str(int(timeToSleep)), "sec: good nap!")
        time.sleep(timeToSleep)
    else:
        if ((oldScoreHome == scoreHome) and (oldScoreAway == scoreAway)):
            if ((time.time() - lastNotif) > notifRefresh):
                periodicNotif()
                lastNotif = time.time()
        else:
            goalNotif()
        time.sleep(periodRefresh)
