py4frc
======

Python code to generate data about FRC events
You put this in your :/Python27/Lib/site-packages/ folder and import it

Single FRC module for Python 2.7
Relies on Beautiful Soup 3 and Numpy (as well as regex and urllib2)

There's a few useful functions, all of which takes the 2013 event codes, 
for example "micmp" for the Michigan State Championship and "casj" for the Silicon Valley Regional.
You can find a full list of codes at frclinks.com (not my site).

getTeamlist(code):
Returns a list of team numbers attending the event
In order of Team Number
E.g. getTeamlist("micmp")
   
getStandings(code):
Returns a list of lists. Each list corresponds to a team with the following format:
[Rank, TeamNum, QS, AP, CP, TP, Record (W-L-T), DQ, Matches Played]
In order of Rank
getStandings("micmp")
  
getRegOpr(code):
Returns a list of OPRs if enough qual matches have been played (else an error message)
In order of Team Number
getRegOpr("micmp")
  
getAllOprs(code):
Returns a dictionary of dictionaries. Each disctionary corresponds to a team.
Each team has the following attributes:
-"OPR"
-"autoOPR"
-"teleOPR"
-"climbOPR"
E.g. getAllOprs("micmp")["2337"]["autoOPR"]
