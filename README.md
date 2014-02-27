py4frc
======

Python code to generate data about FRC events
You put this in your :/Python27/Lib/site-packages/ folder and import it

Single FRC module for Python 2.7
Relies on Beautiful Soup 3 and Numpy (as well as regex and urllib2)

There's a few useful functions, all of which take the 2014 event codes, 
for example "micmp" for the Michigan State Championship and "casj" for the Silicon Valley Regional.
They all also take 
You can find a full list of codes at frclinks.com (not my site).

getTeamlist(code):
Returns a list of team numbers attending the event in order of Team Number 
E.g. getTeamlist("micen")
   
getStandings(code):
Returns a list of lists. Each list corresponds to a team with the following format: 
Rank, TeamNum, QS, Assist, Auto, T&C, Foul, Record, DQ, Played
In order of rank. 
E.g. getStandings("onto")
  
getRegOpr(code):
Eeturns a list of OPRs if enough qual matches have been played (else an error message) in order of Team Number
E.g. getRegOpr("micmp")
  
getAllOprs(code):
Returns a dictionary of dictionaries. Each disctionary corresponds to a team.
Each team has the following attributes:
-"OPR" 
-"autoOPR" 
-"assistOPR" 
-"trussOPR" 
-"foulOPR
E.g. getAllOprs("micmp")["2337"]["autoOPR"]
