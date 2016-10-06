import nfldb
import numpy
import sys

from collections import defaultdict
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

def calculateOdds( history, total, gc ):
    "Calculate the odds of winning spread"
    over = 0
    push = 0
    under = 0
    for r in history:
        if r == total:
            push = percentage(history[r],gc)
        elif r < total:
            under += percentage(history[r],gc)
        else:
            over += percentage(history[r],gc)
    
    print 'Chances of outcome for a total of',total,'\n'
    print 'Over : ','{:02.2f}%'.format(over)
    print 'Push : ','{:02.2f}%'.format(push)
    print 'Under: ','{:02.2f}%'.format(under),'\n'
    print 'O+P  : ','{:02.2f}%'.format(over + push)
    print 'U+P  : ','{:02.2f}%'.format(under + push),'\n'
        
scoreHistory = list()

for g in q.sort('start_time').as_games():
    total_score = g.home_score + g.away_score
    scoreHistory.append(total_score)

d = defaultdict(int)
gameCount = 0
for score in scoreHistory:
    d[score] += 1
    gameCount += 1

if (len(sys.argv)>1):
    calculateOdds (d, int(sys.argv[1]), gameCount)
else:
    printOdds(d, gameCount)

