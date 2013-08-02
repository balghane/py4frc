#-------------------------------------------------------------------------------
# Name:        FRC
# Purpose:     Module to simplify getting standings, match results, and OPRs
#               from the FIRST web pages
# Author:      BaselA
#-------------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
import urllib2
import re
from numpy.linalg import cholesky
from numpy.linalg import solve
from numpy import *

def frclinksTo(code, whatDoYouWant):
    if whatDoYouWant == "None":
        url = "http://frclinks.frclinks.com/e/"+str(code)
    elif whatDoYouWant == "m" or whatDoYouWant == "r":
        url = "http://frclinks.frclinks.com/e/"+str(whatDoYouWant)+"/"+str(code)
    soup = BeautifulSoup(urllib2.urlopen(url))
    return soup.findAll('script')[2].getText()[19:-2]

def getTeamlist(code):
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "None")))
    teams = []
    for team in soup.body.center.table.tr.td.p.center.table.tr.td.findAll('a')[5:]:
        teams.append(team.getText())
    return teams

def removeBlanks(array):
    while True:
        try:
            if array[-1][9] == "" or array[-1][9] == "&nbsp;":
                array.pop()
            else:
                return array
        except IndexError:
            try:
                array.pop()
            except IndexError:
                return []

def getMatches(code):
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code,"m")))
    values = []
    quals= []
    for match in soup.findAll('tr', {"style":"background-color:#FFFFFF;"}) + soup.findAll('tr', {"style": re.compile('mso-yfti-irow:[0-9]')})[6:-3]:
        if re.search('(E|D|T)', match.td.getText()[0]):
            pass
        else:
            for value in match:
                if isinstance(value, basestring):
                    pass
                else:
                    values.append(value.getText())
            quals.append(values)
            values = []
    elims = []
    try:
        quals[-1][1]
    except IndexError:
        del(quals[-1])
    while re.search('(i|t)', quals[-1][1]):
      elims.append(quals.pop())
    elims.reverse()
    for match in elims:
        del match[1]
    quals = removeBlanks(quals)
    elims = removeBlanks(elims)
    return quals, elims

def getStandings(code):
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "r")))
    standings = []
    for team in soup.findAll('tr', {"style":"background-color:#FFFFFF;"}):
      values = []
      for value in team:
         try:
            values.append(value.getText())
         except AttributeError:
            pass
      standings.append(values)
    return standings

def getOprMatrix(code):
    teamList = getTeamlist(code)
    teamDict={}

    for team in teamList:
        otherTeamList = {"totalScore":0}
        for otherTeam in teamList:
            otherTeamList[otherTeam] = 0
        teamDict[team] = otherTeamList

    alliances=[]
    scores =[]

    for matchNum, match in enumerate(getMatches(code)[0]):
        redData=match[2:5]
        scores.append(match[8])
        blueData=match[5:8]
        scores.append(match[9])
        alliances.append(redData)
        alliances.append(blueData)

    for allianceNum, alliance in enumerate(alliances):
        for team in alliance:
            teamDict[team][alliance[0]] = teamDict[team][alliance[0]] + 1
            teamDict[team][alliance[1]] = teamDict[team][alliance[1]] + 1
            teamDict[team][alliance[2]] = teamDict[team][alliance[2]] + 1
            teamDict[team]["totalScore"] = teamDict[team]["totalScore"] + int(scores[allianceNum])

    oprMatrix =[]
    teamScores = []

    for team in teamList:
        oprMatrixLine = []
        for otherTeam in teamList:
            oprMatrixLine.append(teamDict[team][otherTeam])
        oprMatrix.append(oprMatrixLine)
        teamScores.append(teamDict[team]["totalScore"])
    return oprMatrix, teamScores

def calcOPR(oprMatrix, scores):
    try:
        L = cholesky(oprMatrix)
        y = solve(L, scores)
        OPR = solve(L.T.conj(), y)
        return OPR
    except BaseException:
        return []
    else:
        return []

def getRegOpr(code):
    oprDict = {}
    OPR = calcOPR(getOprMatrix(code)[0],getOprMatrix(code)[1])
    if OPR == []:
        raise Exception("Check again in "+str(len(getTeamlist(code))-len(getOprMatrix(code)[1])/2)+" matches")
        return
    for teamNum, team in enumerate(getTeamlist(code)):
        oprDict[team] = OPR[teamNum]
    return OPR

def getAllOprs(code):
    oprMatrix, totalScores = getOprMatrix(code)
    teamDict={}
    autoScores = []
    teleScores = []
    climbScores = []
    for teamNum, team in enumerate(getStandings(code)):
        teamDict[team[1]] = {"autoScore":team[3], "teleScore":team[5], "climbScore":team[4]}
        autoScores.append(teamDict[team[1]]["autoScore"])
        teleScores.append(teamDict[team[1]]["teleScore"])
        climbScores.append(teamDict[team[1]]["climbScore"])
    totOPR = calcOPR(oprMatrix, totalScores)
    autoOPR = calcOPR(oprMatrix, autoScores)
    teleOPR = calcOPR(oprMatrix, teleScores)
    climbOPR = calcOPR(oprMatrix, climbScores)

    for value in range(len(totOPR)):
        x = totOPR[value]/(autoOPR[value]+teleOPR[value]+climbOPR[value])
        autoOPR[value] = x*autoOPR[value]
        teleOPR[value] = x*teleOPR[value]
        climbOPR[value] = x*climbOPR[value]

    oprDict={}
    for teamNum, team in enumerate(getTeamlist(code)):
        oprDict[team] = {"OPR":totOPR[teamNum], "autoOPR":autoOPR[teamNum], "teleOPR":teleOPR[teamNum], "climbOPR":climbOPR[teamNum]}

    for team in oprDict:
        shift = oprDict[team]["OPR"]-(oprDict[team]["autoOPR"]+oprDict[team]["teleOPR"]+oprDict[team]["climbOPR"])
        oprSum = abs(oprDict[team]["autoOPR"])+abs(oprDict[team]["teleOPR"])+abs(oprDict[team]["climbOPR"])
        for oprType in ["autoOPR", "teleOPR", "climbOPR"]:
            oprDict[team][oprType] +=(shift/oprSum)*abs(oprDict[team][oprType])

    return oprDict
