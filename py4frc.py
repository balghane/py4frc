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
import numpy

eventInfo = {'code': {'week': '6', 'code': 'code', 'name': 'Colorado'},
'mdba': {'week': '6', 'code': 'mdba', 'name': 'Chesapeake'},
'ctgro': {'week': '2', 'code': 'ctgro', 'name': 'Groton'},
'waamv': {'week': '1', 'code': 'waamv', 'name': 'Auburn Mountainview'},
'wamou': {'week': '3', 'code': 'wamou', 'name': 'Mt. Vernon'},
'washo': {'week': '4', 'code': 'washo', 'name': 'Shorewood'},
'vari': {'week': '4', 'code': 'vari', 'name': 'Virginia'},
'mitry': {'week': '6', 'code': 'mitry', 'name': 'Troy'},
'lake': {'week': '6', 'code': 'lake', 'name': 'Bayou'},
'njbri': {'week': '5', 'code': 'njbri', 'name': 'Bridgewater-Raritan'},
'nytr': {'week': '3', 'code': 'nytr', 'name': 'New York Tech Valley'},
'nyli': {'week': '5', 'code': 'nyli', 'name': 'SBPLI Long Island'},
'okok': {'week': '5', 'code': 'okok', 'name': 'Oklahoma'},
'onwi': {'week': '6', 'code': 'onwi', 'name': 'Windsor Essex Great Lakes'},
'azch': {'week': '4', 'code': 'azch', 'name': 'Arizona'},
'ilch': {'week': '6', 'code': 'ilch', 'name': 'Midwest'},
'txho': {'week': '6', 'code': 'txho', 'name': 'Lone Star'},
'mndu': {'week': '2', 'code': 'mndu', 'name': 'Lake Superior'},
'gadu': {'week': '5', 'code': 'gadu', 'name': 'Peachtree'},
'ncre': {'week': '3', 'code': 'ncre', 'name': 'North Carolina'},
'onwa': {'week': '4', 'code': 'onwa', 'name': 'Waterloo'},
'misou': {'week': '1', 'code': 'misou', 'name': 'Southfield'},
'mrcmp': {'week': '7', 'code': 'mrcmp', 'name': 'Mid-Atlantic Robotics FRC Region Championship'},
'melew': {'week': '6', 'code': 'melew', 'name': 'Pine Tree'},
'milan': {'week': '6', 'code': 'milan', 'name': 'Lansing'},
'mxmc': {'week': '3', 'code': 'mxmc', 'name': 'Mexico City'},
'nyny': {'week': '6', 'code': 'nyny', 'name': 'New York City'},
'arfa': {'week': '2', 'code': 'arfa', 'name': 'Arkansas'},
'qcmo': {'week': '4', 'code': 'qcmo', 'name': 'Festival de Robotique FRC a Montreal'},
'miwmi': {'week': '4', 'code': 'miwmi', 'name': 'West Michigan'},
'scmb': {'week': '1', 'code': 'scmb', 'name': 'Palmetto'},
'onnb': {'week': '5', 'code': 'onnb', 'name': 'North Bay'},
'mosl': {'week': '3', 'code': 'mosl', 'name': 'St. Louis'},
'orosu': {'week': '6', 'code': 'orosu', 'name': 'Oregon State University'},
'pahat': {'week': '1', 'code': 'pahat', 'name': 'Hatboro-Horsham'},
'dcwa': {'week': '5', 'code': 'dcwa', 'name': 'Greater DC'},
'wache': {'week': '3', 'code': 'wache', 'name': 'Eastern Washington University'},
'ctsou': {'week': '4', 'code': 'ctsou', 'name': 'Southington'},
'nhnas': {'week': '1', 'code': 'nhnas', 'name': 'Granite State'},
'onto2': {'week': '1', 'code': 'onto2', 'name': 'Greater Toronto West'},
'orore': {'week': '2', 'code': 'orore', 'name': 'Oregon City'},
'nhdur': {'week': '2', 'code': 'nhdur', 'name': 'UNH'},
'inwl': {'week': '4', 'code': 'inwl', 'name': 'Boilermaker'},
'misjo': {'week': '5', 'code': 'misjo', 'name': 'St. Joseph'},
'rismi': {'week': '4', 'code': 'rismi', 'name': 'Rhode Island'},
'onto': {'week': '2', 'code': 'onto', 'name': 'Greater Toronto East'},
'necmp': {'week': '7', 'code': 'necmp', 'name': 'New England FRC Region Championship'},
'mitvc': {'week': '4', 'code': 'mitvc', 'name': 'Traverse City'},
'mawor': {'week': '3', 'code': 'mawor', 'name': 'WPI'},
'inth': {'week': '2', 'code': 'inth', 'name': 'Crossroads'},
'mndu2': {'week': '2', 'code': 'mndu2', 'name': 'Northern Lights'},
'flfo': {'week': '6', 'code': 'flfo', 'name': 'South Florida'},
'miket': {'week': '2', 'code': 'miket', 'name': 'Kettering University'},
'mihow': {'week': '3', 'code': 'mihow', 'name': 'Howell'},
'waell': {'week': '5', 'code': 'waell', 'name': 'Central Washington University'},
'wimi': {'week': '4', 'code': 'wimi', 'name': 'Wisconsin'},
'calb': {'week': '4', 'code': 'calb', 'name': 'Los Angeles'},
'casd': {'week': '2', 'code': 'casd', 'name': 'San Diego'},
'miliv': {'week': '5', 'code': 'miliv', 'name': 'Livonia'},
'casa': {'week': '3', 'code': 'casa', 'name': 'Sacramento'},
'casb': {'week': '1', 'code': 'casb', 'name': 'Inland Empire'},
'mabos': {'week': '5', 'code': 'mabos', 'name': 'Northeastern University'},
'casj': {'week': '6', 'code': 'casj', 'name': 'Silicon Valley'},
'txlu': {'week': '2', 'code': 'txlu', 'name': 'Hub City'},
'mibed': {'week': '6', 'code': 'mibed', 'name': 'Bedford'},
'txsa': {'week': '1', 'code': 'txsa', 'name': 'Alamo'},
'nvlv': {'week': '6', 'code': 'nvlv', 'name': 'Las Vegas'},
'txda': {'week': '3', 'code': 'txda', 'name': 'Dallas'},
'migul': {'week': '2', 'code': 'migul', 'name': 'Gull Lake'},
'abca': {'week': '6', 'code': 'abca', 'name': 'Western Canada'},
'pncmp': {'week': '7', 'code': 'pncmp', 'name': 'Autodesk FRC Championship'},
'orwil': {'week': '4', 'code': 'orwil', 'name': 'Wilsonville'},
'utwv': {'week': '3', 'code': 'utwv', 'name': 'Utah'},
'wasno': {'week': '2', 'code': 'wasno', 'name': 'Glacier Peak'},
'njfla': {'week': '1', 'code': 'njfla', 'name': 'Mt. Olive'},
'ista': {'week': '6', 'code': 'ista', 'name': 'Israel'},
'nyro': {'week': '5', 'code': 'nyro', 'name': 'Finger Lakes'},
'ilil': {'week': '1', 'code': 'ilil', 'name': 'Central Illinois'},
'mnmi': {'week': '5', 'code': 'mnmi', 'name': 'Minnesota 10000 Lakes'},
'njtab': {'week': '4', 'code': 'njtab', 'name': 'Lenape-Seneca'},
'miwat': {'week': '5', 'code': 'miwat', 'name': 'Waterford'},
'hiho': {'week': '5', 'code': 'hiho', 'name': 'Hawaii'},
'njcli': {'week': '3', 'code': 'njcli', 'name': 'Clifton'},
'papi': {'week': '5', 'code': 'papi', 'name': 'Greater Pittsburgh'},
'ohci': {'week': '5', 'code': 'ohci', 'name': 'Queen City'},
'ohcl': {'week': '4', 'code': 'ohcl', 'name': 'Buckeye'},
'miesc': {'week': '3', 'code': 'miesc', 'name': 'Escanaba'},
'tnkn': {'week': '5', 'code': 'tnkn', 'name': 'Smoky Mountains'},
'mokc': {'week': '3', 'code': 'mokc', 'name': 'Greater Kansas City'},
'cthar': {'week': '5', 'code': 'cthar', 'name': 'Hartford'},
'flor': {'week': '3', 'code': 'flor', 'name': 'Orlando'},
'paphi': {'week': '3', 'code': 'paphi', 'name': 'Springside Chestnut Hill'},
'micen': {'week': '1', 'code': 'micen', 'name': 'Center Line'},
'mimid': {'week': '4', 'code': 'mimid', 'name': 'Great Lakes Bay Region'},
'mnmi2': {'week': '5', 'code': 'mnmi2', 'name': 'Minnesota North Star'},
'micmp': {'week': '7', 'code': 'micmp', 'name': 'Michigan FRC State Championship'},
'cama': {'week': '2', 'code': 'cama', 'name': 'Central Valley'}}

codes =['abca','arc','arfa','azch','calb','cama','casa','casb','casd','casj',
'cmp','code','ctgro','cthar','ctsou','cur','dcwa','flfo','flor','gadu','gal',
'hiho','ilch','ilil','inth','inwl','ista','lake','mabos','mawor','mdba','melew',
'mibed','micen','micmp','miesc','migul','mihow','miket','milan','miliv','mimid',
'misjo','misou','mitry','mitvc','miwat','miwmi','mndu','mndu2','mnmi','mnmi2',
'mokc','mosl','mrcmp','mxmc','ncre','necmp','new','nhdur','nhnas','njbri','njcli',
'njfla','njtab','nvlv','nyli','nyny','nyro','nytr','ochl','ohci','okok','onnb',
'onto','onto2','onwa','onwi','orore','orosu','orwil','pahat','paphi','papi',
'pncmp','qcmo','rismi','scmb','tnkn','txda','txho','txlu','txsa','utwv','vari',
'waahs','waamv','wache','waell','wamou','washo','wasno','wimi']

abbreviations = {'abca':'abca','wcr':'abca','westcanada':'abca','westerncanada':'abca',
'westerncanadian':'abca','arc':'arc','archimedes':'arc','arfa':'arfa','razorback':'arfa',
'arkansas':'arfa','azch':'azch','phoenix':'azch','arizona':'azch','calb':'calb',
'losangeles':'calb','LA':'calb','cama':'cama','centralvalley':'cama','cvr':'cama',
'casa':'casa','sacramento':'casa','casb':'casb','inlandempire':'casb','casd':'casd',
'sandiego':'casd','casj':'casj','siliconvalley':'casj','svr':'casj','championship':'cmp',
'cmp':'cmp','einstein':'cmp','code':'code','colorado':'code','groton':'ctgro','ctgro':'ctgro',
'connecticut':'cthar','cthar':'cthar','hartford':'cthar','ctha':'cthar','southington':'ctsou',
'ctsou':'ctsou','cur':'cur','curie':'cur','dc':'dcwa','dcwa':'dcwa','washington':'dcwa',
'washingtondc':'dcwa','flbr':'flfo','southflorida':'flfo','flor':'flor','orlando':'flor',
'gadu':'gadu','peachtree':'gadu','gal':'gal','galileo':'gal','hawaii':'hiho','hiho':'hiho',
'ilch':'ilch','midwest':'ilch','ilil':'ilil','centralillinois':'ilil','centralil':'ilil',
'centillinois':'ilil','centil':'ilil','crossroads':'inth','inth':'inth','bmr':'inwl',
'boilermaker':'inwl','inwl':'inwl','israel':'ista','isreal':'ista','ista':'ista',
'bayou':'lake','lake':'lake','boston':'mabos','mabos':'mabos','mabo':'mabos',
'northeastern':'mabos','mawo':'mawor','wpi':'mawor','mawor':'mawor','chesapeake':'mdba',
'mdba':'mdba','mele':'melew','pine tree':'melew','ptr':'melew','melew':'melew',
'bedford':'mibed','mibed':'mibed','centerline':'micen','micen':'micen',
'michiganstatechampionship':'micmp','micmp':'micmp','msc':'micmp','escanaba':'miesc',
'miesc':'miesc','gulllake':'migul','migul':'migul','howell':'mihow','mihow':'mihow',
'kettering':'miket','ketteringuniversity':'miket','miket':'miket','lansing':'milan',
'milan':'milan','livonia':'miliv','miliv':'miliv','mimid':'mimid','greatlakesbay':'mimid',
'greatlakesbayregion':'mimid','greatlakes':'mimid','misou':'misou','Southfield':'misou',
'misjo':'misjo','stjoe':'misjo','stjoseph':'misjo','mitry':'mitry','troy':'mitry',
'mitvc':'mitvc','tc':'mitvc','traversecity':'mitvc','miwfd':'miwat','waterford':'miwat',
'miwat':'miwat','miwmi':'miwmi','westmichigan':'miwmi','wmr':'miwmi','lakesuperior':'mndu',
'mndu':'mndu','mndu2':'mndu2','northernlights':'mndu2','10000lakes':'mnmi',
'10klakes':'mnmi','mnmi':'mnmi','minnesotanorthstar':'mnmi2','mnmi2':'mnmi2',
'northstar':'mnmi2','greaterkansascity':'mokc','kansascity':'mokc','kc':'mokc',
'kcr':'mokc','mokc':'mokc','mosl':'mosl','stlouis':'mosl','lehigh':'mrcmp',
'mar':'mrcmp','marcmp':'mrcmp','mrcmp':'mrcmp','mexico':'mxmc','mexicocity':'mxmc',
'mxmc':'mxmc','ncr':'ncre','ncre':'ncre','northcarolina':'ncre','new':'new',
'newton':'new','newenglandcmp':'necmp','newenglandchampionship':'necmp',
'necmp':'necmp','nechampionship':'necmp','ne':'necmp','nhdur':'nhdur','unh':'nhdur',
'bae':'nhnas','baegranitestate':'nhnas','granitestate':'nhnas','gsr':'nhnas',
'nhma':'nhnas','nhnas':'nhnas','br':'njbri','bridgewater':'njbri',
'bridgewaterraritan':'njbri','njbrg':'njbri','njbri':'njbri','clifton':'njcli',
'njcli':'njcli','flanders':'njfla','mountolive':'njfla','mtolive':'njfla',
'njfla':'njfla','lenape':'njtab','lenapeseneca':'njtab','njlen':'njtab',
'njtab':'njtab','lasvegas':'nvlv','lvr':'nvlv','nvlv':'nvlv','vegas':'nvlv',
'longisland':'nyli','nyli':'nyli','sbplilongisland':'nyli','sbpli':'nyli',
'newyorkcity':'nyny','nyc':'nyny','nyny':'nyny','fingerlakes':'nyro','flr':'nyro',
'nyro':'nyro','newyorktechvalley':'nytr','techvalley':'nytr','nytr':'nytr',
'ohic':'ohci','qcr':'ohci','queencity':'ohci','ohci':'ohci','buckeye':'ohcl',
'ohcl':'ohcl','oklahoma':'okok','okok':'okok','okc':'okok','northbay':'onnb',
'onnb':'onnb','greatertorontoeast':'onto','gtre':'onto','onto':'onto',
'torontoeast':'onto','greatertorontowest':'onto2','gtrw':'onto2','onto2':'onto2',
'torontowest':'onto2','onwa':'onwa','waterloo':'onwa','onwi':'onwi','windsor':'onwi',
'windsoressex':'onwi','oregoncity':'orore','orore':'orore','oregonstate':'orosu',
'orosu':'orosu','wilsonville':'orwil','orwil':'orwil','hatborohorsham':'pahat',
'hh':'pahat','pahat':'pahat','chestnuthill':'paphi','paphi':'paphi','springside':'paphi',
'springsidechestnuthill':'paphi','papi':'papi','pittsburgh':'papi','pnw':'pncmp',
'pacificcmp':'pncmp','pacificnorthwestcmp':'pncmp','pnwcmp':'pncmp',
'pncmp':'pncmp','montreal':'qcmo','qcmo':'qcmo','rhodeisland':'rismi',
'rismi':'rismi','palmetto':'scmb','scmb':'scmb','smokymountains':'tnkn',
'smr':'tnkn','tnkn':'tnkn','dallas':'txda','txda':'txda','lonestar':'txho',
'lsr':'txho','txho':'txho','hubcity':'txlu','txlu':'txlu','alamo':'txsa',
'txsa':'txsa','utah':'utwv','utwv':'utwv','vari':'vari','virginia':'vari',
'auburn':'waahs','waahs':'waahs','auburnmtn':'waamv','auburnmountainview':'waamv',
'waamv':'waamv','centralwash':'waell','centralwashington':'waell','waell':'waell',
'mtvernon':'wamou','wamou':'wamou','spokane':'wache','wach':'wache','wasche':'wache',
'eastwash':'wache','eastwashington':'wache','easternwash':'wache','easternwashington':'wache',
'wache':'wache','shorewood':'washo','washo':'washo','glacierpeak':'wasno',
'wasno':'wasno','wimi':'wimi','wisconsin':'wimi'}

def getCode(phrase):
    phrase = phrase.lower()
    for code in codes:
        if phrase == code:
            return code
    while search('[ -\.]', phrase):
        phrase = sub("[ -\.]", "", phrase)
    phrase = sub("district", "", sub("regional", "", phrase))
    for abbrev in abbreviations:
        if phrase == abbrev:
            return abbreviations[abbrev]

def frclinksTo(code, whatDoYouWant, year):
    code = getCode(code)
    if whatDoYouWant == "None":
        url = "http://frclinks.frclinks.com/e/"+str(code)
    elif whatDoYouWant == "m" or whatDoYouWant == "r":
        url = "http://frclinks.frclinks.com/e/"+str(whatDoYouWant)+"/"+str(code)
    if year != 2014:
        url = url + "/"+str(year)
    soup = BeautifulSoup(urllib2.urlopen(url))
    return soup.findAll('script')[2].getText()[19:-2]

def getTeamlist(code):
    code = getCode(code)
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "None", 2014)))
    teams = []
    for team in soup.body.center.table.tr.td.p.center.table.tr.td.findAll('a')[5:]:
        teams.append(team.getText())
    return teams

def getTeamStandings(code):
    code = getCode(code)
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "r", 2014)))
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
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code,"m", 2014)))
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
    soup = BeautifulSoup(urllib2.urlopen(frclinksTo(code, "r", 2014)))
    standings = []
    for team in soup.findAll('tr', {"style":"background-color:#FFFFFF;"}):
      values = []
      for value in team:
         try:
            values.append(value.getText())
         except AttributeError:
            pass
      values[6]=float(values[6])-float(values[5])-float(values[3])
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
    try:
        L = cholesky(oprMatrix)
        y = solve(L, scores)
        OPR = solve(L.T.conj(), y)
    except numpy.linalg.LinAlgError:
        return []
    return OPR

def getRegOpr(code):
    code = getCode(code)
    oprMatrix, scores = getOprMatrix(code)
    OPR = calcOPR(oprMatrix, scores)
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
    assistScores = []
    trussScores = []
    foulScores = []
    teamlist = getTeamStandings(code)
    for teamNum, team in enumerate(getStandings(code)):
        teamDict[team[1]] = {"autoScore":team[4], "assistScore":team[3], "trussScore":team[5], "foulScore":team[6]}

    for team in teamlist:
        autoScores.append(teamDict[team]["autoScore"])
        assistScores.append(teamDict[team]["assistScore"])
        trussScores.append(teamDict[team]["trussScore"])
        foulScores.append(teamDict[team]["foulScore"])

    totOPR = calcOPR(oprMatrix, totalScores)
    autoOPR = calcOPR(oprMatrix, autoScores)
    assistOPR = calcOPR(oprMatrix, assistScores)
    trussOPR = calcOPR(oprMatrix, trussScores)
    foulOPR = calcOPR(oprMatrix, foulScores)

    oprDict={}
    try:
        for teamNum, team in enumerate(getTeamStandings(code)):
            oprDict[team] = {"OPR":totOPR[teamNum], "autoOPR":autoOPR[teamNum], "assistOPR":assistOPR[teamNum], "trussOPR":trussOPR[teamNum], "foulOPR":foulOPR[teamNum]}

        for team in oprDict:
            shift = oprDict[team]["OPR"]-(oprDict[team]["autoOPR"]+oprDict[team]["assistOPR"]+oprDict[team]["trussOPR"]+oprDict[team]["foulOPR"])
            oprSum = abs(oprDict[team]["autoOPR"])+abs(oprDict[team]["assistOPR"])+abs(oprDict[team]["trussOPR"])+abs(oprDict[team]["foulOPR"])
            for oprType in ["autoOPR", "assistOPR", "foulOPR"]:
                oprDict[team][oprType] +=(shift/oprSum)*abs(oprDict[team][oprType])

        for team in oprDict:
            for value in oprDict[team]:
                oprDict[team][value] = round(float(oprDict[team][value]),2)
    except IndexError:
        pass
    return oprDict

def main():
    while True:
        print "To get the teamlist for an event, type 'teams'"
        print "To get the team OPRs for an event, type 'opr'"
        print "To get all the team OPR subtypes for an event, type 'allopr'"
        print "To get the standings for an event, type 'standings'"
        want = raw_input("What do you want? ").lower()
        while search('[ -\.]', want):
            want = sub("[ -\.]", "", want)
        if search("allopr", want):
            code = getCode(raw_input("What event? "))
            opr = getAllOprs(code)
            teams = getTeamStandings(code)
            print "\t".join(["Team", "OPR ", "autoOPR", "assistOPR", "trussOPR", "foulOPR"])
            for team in teams:
                print "\t".join([team+int(4-len(team))*" ", str(opr[team]["OPR"]), str(opr[team]["autoOPR"]), str(opr[team]["teleOPR"]), str(opr[team]["climbOPR"])])
        elif search("opr", want):
            code = getCode(raw_input("What event? "))
            opr = getRegOpr(code)
            for i,team in enumerate(getTeamStandings(code)):
                print team, opr[i]
        elif search("team(s|list)", want):
            code = getCode(raw_input("What event? "))
            teams = getTeamlist(code)
            for team in teams:
                print team
        elif search("(standing|ranking)", want):
            code = getCode(raw_input("What event? "))
            standings = getStandings(code)
            print "\t".join(["Rank", "Team", "QP  ","AP  ", "CP  ", "TP  ", "Record", "DQ", "Played"])
            for team in standings:
                team[0] += int(4-len(team[0]))*" "
                if len(team[1]) < 4:
                    team[1] += int(4-len(team[1]))*" "
                print "\t".join(team)
        else:
            print "I'm not sure what you mean. Try again?"


if __name__ == "__main__":
    main()
