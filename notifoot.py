"""
Notifoot: follow your favorite matches while working!
"""

from plyer import notification
import json
import requests
import time
from datetime import datetime as dt

# Constants
periodRefresh = 10
notifRefresh = 300
timeZone_sec = 3600

# Useful variables (will be refreshed)
scoreHome = []
scoreAway = []
dateOfStart = []
nothing = []
lastNotif = 0
firstRun = True


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
        timeout=30
    )


def refreshScore():
    apiUrl = "https://worldcupjson.net/matches/today?by_date=asc"
    urlDump = requests.get(apiUrl).text
    # Debug code.
    # jsonPath = "test.json"
    # with open(jsonPath, "r") as f:
    #     fileDump = f.readlines()
    # urlDump = ""
    # for line in fileDump:
    #     urlDump += line
    jsonData = json.loads(urlDump)
    nbMatches = len(jsonData)
    for i in range(nbMatches):
        teamHome.append(jsonData[i]['home_team']['country'])
        teamAway.append(jsonData[i]['away_team']['country'])
        scoreHome.append(jsonData[i]['home_team']['goals'])
        scoreAway.append(jsonData[i]['away_team']['goals'])
        timeMatch.append(jsonData[i]['time'])
        dateOfStart.append(jsonData[i]['datetime'])


def compareTables(T1, T2):
    """ True if Same size and same values """
    res = True
    if len(T1) == len(T2):
        for i in range(len(T1)):
            res *= (T1[i] == T2[i])
    else:
        res = False
    return res


while (True):
    timeMatch = []
    teamHome = []
    teamAway = []
    dateOfStart = []
    oldScoreHome = [x for x in scoreHome]
    oldScoreAway = [x for x in scoreAway]
    scoreHome = []
    scoreAway = []
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
        if (timeToSleep > 0):
            time.sleep(timeToSleep)
    else:
        # True if same score, False if evolution
        areTheScoresTheSame = compareTables(
            oldScoreHome, scoreHome) * compareTables(oldScoreAway, scoreAway)
        if (areTheScoresTheSame > 0) or (firstRun is True):
            if ((time.time() - lastNotif) > notifRefresh):
                periodicNotif()
                lastNotif = time.time()
        else:
            # Different score: flash notif
            goalNotif()
        time.sleep(periodRefresh)
    firstRun = False
