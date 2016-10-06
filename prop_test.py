import nfldb

db = nfldb.connect()
q = nfldb.Query(db)
q.player(full_name='Andrew Luck')
q.game(season_year=2016, season_type='Regular')
for pp in q.sort('passing_yds').as_games():  # .ilimit(5).as_aggregate():
    print pp.player, pp.passing_yds
