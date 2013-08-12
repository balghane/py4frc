#-------------------------------------------------------------------------------
# Name:        FRC
# Purpose:     Module to simplify getting standings, match results, and OPRs
#               from the FIRST web pages
# Author:      BaselA
#-------------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
import urllib2
from re import search
from re import sub
from re import compile
from numpy.linalg import solve
from numpy.linalg import cholesky
from numpy import transpose

def getCode(phrase):
    codes =['txsa','orpo','nhma','lake','mibed','inwl','mabo','njbrg','ohcl',
    'cama','wase2','mdba','code','ctha','inth','txda','midet','qcmo','nyro',
    'migbl','mokc','onto','onto2','migul','pahat','hiho','txlu','casb','ista',
    'miket','mndu','nvlv','njlen','miliv','txho','calb','micmp','mrcmp','ilch',
    'mnmi','mnmi2','njfla','nyny','ncre','mndu2','okok','flor','scmb','gadu',
    'azch','mele','papi','ohic','arfa','casa','casd','nyli','wase','casj','tnkn',
    'flbr','wach','paphi','misjo','mosl','njewn','mitvc','mitry','utwv','vari',
    'dcwa','miwfd','onwa','miwmi','abca','wimi','mawo','cmp','arc','cur','gal',
    'new']
    phrase = phrase.lower()
    for code in codes:
        if phrase == code:
            return code
    abbreviations = {
    'alamo':'txsa','lakesuperior':'mndu','stjoe':'misjo','springsidechestnuthill':'paphi',
    'autodeskoregon':'orpo','lasvegas':'nvlv','washington':'dcwa','stjoseph':'misjo',
    'baegranitestate':'nhma','lenapeseneca':'njlen','westerncanada':'abca','stlouis':'mosl',
    'bayou':'lake','livonia':'miliv','westcanada':'abca','tcnj':'njewn',
    'bedford':'mibed','lonestar':'txho','archimedes':'arc','traversecity':'mitvc',
    'boilermaker':'inwl','losangeles':'calb','curie':'cur','troy':'mitry',
    'boston':'mabo','michiganstatechampionship':'micmp','galileo':'gal','utah':'utwv',
    'bridgewaterraritan':'njbrg','midatlanticregionchampionship':'mrcmp','newton':'new','virginia':'vari',
    'buckeye':'ohcl','midwest':'ilch','einstein':'cmp','washingtondc':'dcwa',
    'centralvalley':'cama','minnesota10000lakes':'mnmi','gsr':'nhma','waterford':'miwfd',
    'centralwashington':'wase2','minnesotanorthstar':'mnmi2','bmr':'inwl','waterloo':'onwa',
    'chesapeake':'mdba','newyorkcity':'nyny','cvr':'cama','westmichigan':'miwmi',
    'colorado':'code','northcarolina':'ncre','cwr':'wase2','westerncanadian':'abca',
    'connecticut':'ctha','northernlights':'mndu2','flr':'nyro','wisconsin':'wimi',
    'crossroads':'inth','oklahoma':'okok','kcr':'mokc','wpi':'mawo',
    'dallas':'txda','orlando':'flor','gtre':'onto','oregon':'orpo',
    'detroit':'midet','palmetto':'scmb','gtrw':'onto2','granitestate':'nhma',
    'montreal':'qcmo','peachtree':'gadu','lvr':'nvlv','bae':'nhma',
    'fingerlakes':'nyro','phoenix':'azch','lsr':'txho','bridgewater':'njbrg',
    'grandblanc':'migbl','pine tree':'mele','msc':'micmp','kansascity':'mokc',
    'greaterkansascity':'mokc','pittsburgh':'papi','marcmp':'mrcmp','torontoeast':'onto',
    'greatertorontoeast':'onto','queencity':'ohic','nyc':'nyny','torontowest':'onto2',
    'greatertorontowest':'onto2','razorback':'arfa','ncr':'ncre','kettering':'miket',
    'gulllake':'migul','sacramento':'casa','ptr':'mele','lenape':'njlen',
    'hatborohorsham':'pahat','sandiego':'casd','qcr':'ohic','10000lakes':'mnmi',
    'hawaii':'hiho','sbplilongisland':'nyli','svr':'casj','northstar':'mnmi2',
    'hubcity':'txlu','seattle':'wase','smr':'tnkn','10klakes':'mnmi',
    'inlandempire':'casb','siliconvalley':'casj','dc':'dcwa','minnesota10klakes':'mnmi',
    'israel':'ista','smokymountains':'tnkn','wmr':'miwmi','longisland':'nyli',
    'ketteringuniversity':'miket','southflorida':'flbr','wcr':'abca','isreal':'ista',
    'midatlanticchampionship':'mrcmp','spokane':'wach','championship':'cmp', 'mar':'mrcmp',
    'vegas':'nvlv','hh':'pahat','tc':"mitvc","mountolive":"njfla","mtolive":"njfla",
    'flanders':'njfla','br':'njbrg','lehigh':'mrcmp','springside':'paphi',
    'chestnuthill':'paphi','ewing':'njewn'
    }
    while search('[ -\.]', phrase):
        phrase = sub("[ -\.]", "", phrase)
    phrase = sub("district", "", sub("regional", "", phrase))
    for abbrev in abbreviations:
        if phrase == abbrev:
            return abbreviations[abbrev]

def frclinksTo(code, whatDoYouWant):
    code = getCode(code)
    if whatDoYouWant == "None":
        url = "http://frclinks.frclinks.com/e/"+str(code)
    elif whatDoYouWant == "m" or whatDoYouWant == "r":
        url = "http://frclinks.frclinks.com/e/"+str(whatDoYouWant)+"/"+str(code)
    soup = BeautifulSoup(urllib2.urlopen(url))
    return soup.findAll('script')[2].getText()[19:-2]

def getTeamlist(code):
    code = getCode(code)
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "None")))
    teams = []
    for team in soup.body.center.table.tr.td.p.center.table.tr.td.findAll('a')[5:]:
        teams.append(team.getText())
    return teams

def getTeamStandings(code):
    code = getCode(code)
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "r")))
    teams = []
    for team in soup.findAll('tr', {"style":"background-color:#FFFFFF;"}):
        for i,value in enumerate(team):
            if i == 3:
                try:
                    teams.append(value.getText())
                except AttributeError:
                    pass
    teams = list(str(z) for z in sorted(int(x) for x in teams))
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
    code = getCode(code)
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code,"m")))
    values = []
    quals= []
    for match in soup.findAll('tr', {"style":"background-color:#FFFFFF;"}) + soup.findAll('tr', {"style": compile('mso-yfti-irow:[0-9]')})[6:-3]:
        if search('(E|D|T)', match.td.getText()[0]):
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

    if code == "cmp":
        while len(quals)>0:
            try:
                if search('(i|t)', quals[-1][1]):
                    elims.append(quals.pop())
            except:
                pass
    else:
        while search('(i|t)', quals[-1][1]):
            elims.append(quals.pop())

    elims.reverse()
    for match in elims:
        del match[1]
    quals = removeBlanks(quals)
    elims = removeBlanks(elims)
    return quals, elims

def getStandings(code):
    code = getCode(code)
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
    code = getCode(code)
    teamList = getTeamStandings(code)
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
    L = cholesky(oprMatrix)
    y = solve(L, scores)
    OPR = solve(transpose(L), y)
    return OPR

def getRegOpr(code):
    code = getCode(code)
    OPR = calcOPR(getOprMatrix(code)[0],getOprMatrix(code)[1])
    if OPR == []:
        return OPR
    for i in range(len(OPR)):
        OPR[i] = round(float(OPR[i]), 2)
    return OPR

def getAllOprs(code):
    code = getCode(code)
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
    for teamNum, team in enumerate(getTeamStandings(code)):
        oprDict[team] = {"OPR":totOPR[teamNum], "autoOPR":autoOPR[teamNum], "teleOPR":teleOPR[teamNum], "climbOPR":climbOPR[teamNum]}

    for team in oprDict:
        shift = oprDict[team]["OPR"]-(oprDict[team]["autoOPR"]+oprDict[team]["teleOPR"]+oprDict[team]["climbOPR"])
        oprSum = abs(oprDict[team]["autoOPR"])+abs(oprDict[team]["teleOPR"])+abs(oprDict[team]["climbOPR"])
        for oprType in ["autoOPR", "teleOPR", "climbOPR"]:
            oprDict[team][oprType] +=(shift/oprSum)*abs(oprDict[team][oprType])

    for team in oprDict:
        for value in oprDict[team]:
            oprDict[team][value] = round(float(oprDict[team][value]),2)

    return oprDict

def main():
    while True:
        want = raw_input("What do you want? ").lower()
        while search('[ -\.]', want):
            want = sub("[ -\.]", "", want)
        if search("allopr", want):
            code = getCode(raw_input("What event? "))
            opr = getAllOprs(code)
            teams = getTeamStandings(code)
            print "\t".join(["Team", "OPR ", "autoOPR", "teleOPR", "climbOPR"])
            for team in teams:
                print "\t".join([team+int(4-len(team))*" ", str(opr[team]["OPR"]), str(opr[team]["autoOPR"]), str(opr[team]["teleOPR"]), str(opr[team]["climbOPR"])])
        elif search("opr", want):
            code = getCode(raw_input("What event? "))
            opr = getRegOpr(code)
            for i,team in enumerate(getTeamStandings(code)):
                print team, opr[i]
        elif search("team(s|list)", want):
            teams = getTeamlist(raw_input("What event? "))
            for team in teams:
                print team
        elif search("(standing|ranking)", want):
            standings = getStandings(raw_input("What event? "))
            print "\t".join(["Rank", "Team", "QP  ","AP  ", "CP  ", "TP  ", "Record", "DQ", "Played"])
            for team in standings:
                team[0] += int(4-len(team[0]))*" "
                if len(team[1]) < 4:
                    team[1] += int(4-len(team[1]))*" "
                print "\t".join(team)

if __name__ == "__main__":
    main()
