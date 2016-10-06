import nfldb
import numpy
from collections import defaultdict
import sys

db = nfldb.connect()

q = nfldb.Query(db)

#q.game(season_year=2016)
q.game(season_type='Regular')
q.game(finished=True)
# q.game(team='NE')
#q.player(full_name='Jeremy Hill')#.play_player(offense_tds=1) 
def median (lst):
    "Return the median of the list provided"
    return numpy.median(numpy.array(lst))

def percentage(part, whole):
    "Return the value percentage part of the whole"
    return 100 * float(part)/float(whole)
        
def printOdds( dic, gc ):
    'Print the odds table'
    for s in sorted(dic, key=dic.get, reverse=True):
        print s,dic[s],'{:02.2f}%'.format(percentage(dic[s],gc))
     
def calculateOdds( history, spread, gc ):
    "Calculate the odds of winning spread"
    win = 0
    push = 0
    loss = 0
    for r in range (1,spread+1):
        if r == spread:
            push = percentage(history[r],gc)
        else:
            win += percentage(history[r],gc)
    loss = 100 - (win + push)
    print 'Chances of winning for a spread of',spread,'\n'
    print 'Win:  ','{:02.2f}%'.format(win)
    print 'Push: ','{:02.2f}%'.format(push),'\n' 
    print 'W+P : ','{:02.2f}%'.format(win + push)
    print 'Loss: ','{:02.2f}%'.format(loss),'\n\n'

spreadHistory = list()

for g in q.sort('start_time').as_games():
    spread = abs(g.home_score - g.away_score)
    spreadHistory.append(spread)

d = defaultdict(int)
gameCount = 0
for score in spreadHistory:
    d[score] += 1
    gameCount += 1

if (len(sys.argv)>1):
    calculateOdds (d, int(sys.argv[1]), gameCount)
else:
    printOdds(d, gameCount)
