import nfldb
import numpy
import sys

# **********************************CONFIG*************************************
# Set the current week number
currentWeek = sys.argv[1] 

# Set the reporting intervals in number of previous games for modeling
gameHistory = [3, 5, 10]
# **********************************END CONFIG*********************************
db = nfldb.connect()

q = nfldb.Query(db)

q.game(season_year=2016)
q.game(season_type='Regular')
#q.game(finished=True)
q.game(week=currentWeek)
# q.game(team='NE')
# q.player(full_name='Julian Edelman').play_player(offense_tds=1)
def getGameHistory ( sTeam, numwks ):
    "This takes a team and the number of weeks and returns 2 lists, ptsScored ptsAllowed"
    ptsScored = list()
    ptsAllowed = list()
    q_Pts = nfldb.Query(db)
    q_Pts.game(season_type='Regular',finished=True,team=sTeam)
    for games in q_Pts.sort('start_time').limit(numwks).as_games():
        #print games
        if games.home_team == sTeam:
            ptsScored.append(games.home_score)
            ptsAllowed.append(games.away_score)
        else:
            ptsScored.append(games.away_score)
            ptsAllowed.append(games.home_score)
    return ptsScored,ptsAllowed

def median (lst):
    "Return the median of the list provided"
    return numpy.median(numpy.array(lst))
        
def modelTotalPointsHTA(hTeam, aTeam, hAvgPts, aAvgPts):
    #This model outputs the home score adjusted total point calculations 

    # Print the header
    print '#',g.away_team,g.home_team,'Tot'
    # Loop through gameHistory for output intervals 
    for x in gameHistory:
        # Fetch the home history
        homePtsScored, homePtsAllowed = getGameHistory(homeTeam,x)
        # Fetch the away history
        awayPtsScored, awayPtsAllowed = getGameHistory(awayTeam,x)
        # Do the calculations
        adjHPS = (median(homePtsScored) + hAvgPts)/2
        adjHPA = (median(homePtsAllowed) + aAvgPts)/2
        adjAPS = (median(awayPtsScored) + aAvgPts)/2
        adjAPA = (median(awayPtsAllowed) + hAvgPts)/2
        homeProj = (adjHPS + adjHPA)/2
        awayProj = (adjAPS + adjAPA)/2
        projTotal = homeProj + awayProj
        # Print the results
        print x,awayProj,homeProj,projTotal

if len(sys.argv) > 2:
    q.game(team=sys.argv[2])

for g in q.sort('start_time').as_games():
    print '\n',g.start_time,"\n"
    # This is an adjustment for JAC/JAX naming issues
    #if g.home_team == 'JAX':
    #    homeTeam = 'JAC'
    #else:
    homeTeam = g.home_team
    #if g.away_team == 'JAX':
    #    awayTeam = 'JAC'
    #else:
    awayTeam = g.away_team
    modelTotalPointsHTA(homeTeam, awayTeam,22,22)
