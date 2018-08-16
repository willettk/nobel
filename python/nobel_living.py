import nobel
import os
import datetime
import cPickle as pickle

nobel_file = 'nobel_dates.pkl'
if os.path.exists(nobel_file):
    with open(nobel_file,'r') as f:
        dates = pickle.load(f)

else:

    api = nobel.Api()
    
    years = [1901 + x for x in range(117)]
    
    dates = []
    yeargood = 0
    for y in years:
        if y % 10 == 0:
            print(y,yeargood)
            yeargood = 0
        try:
            prize = api.prizes.get(category='literature',year=y)
            laureate = api.laureates.get(id=prize.laureates[0].id)
            dates.append(('w',' '.join((laureate.firstname,laureate.surname)).encode('utf-8').strip(),datetime.date(int(y),10,10)))
            if laureate.died is not None:
                dates.append(('d',' '.join((laureate.firstname,laureate.surname)).encode('utf-8').strip(),laureate.died))
            yeargood +=1 
        except:
            pass
    
    with open(nobel_file,'w') as f:
        pickle.dump(dates,f)

dates_sorted = sorted(dates, key = lambda x: x[2])

alive = 0
max_alive = 0
min_alive = 15

living_stack = []
posthumous = []

_d = []
_n = []

for d in dates_sorted:
    if d[0] == 'w' and d[1] not in posthumous:
        alive += 1
        living_stack.append(d[1])
        last_award = d
    elif d[0] == 'w' and d[1] in posthumous: 
        posthumous.remove(d[1])
    elif d[0] == 'd':
        alive -= 1
        last_death = d
        try:
            living_stack.remove(d[1])
        except ValueError:
            posthumous.append(d[1])

    _d.append(d[2])
    _n.append(alive)
    if alive > max_alive:
        max_alive = alive
        max_stack = living_stack[::]
        latest_addition = last_award

    # Fewest alive since WWII

    if (alive < min_alive) and d[2].year > 1940:
        min_alive = alive
        min_stack = living_stack[::]
        min_latest_death = last_death

ind = dates_sorted.index(latest_addition)
if ind < len(dates_sorted) - 1:
    latest_death = dates_sorted[ind+1]
    print "\n{:d} laureates were alive between awarding of the prize to \n{} ({})\nand the death of \n{} ({}).\n".format(max_alive,
                                                latest_addition[1],latest_addition[2],
                                                latest_death[1],latest_death[2])
else:
    print "{:d} laureates alive since awarding the prize to {} ({}).".format(max_alive,
                                                latest_addition[1],latest_addition[2])
                                                                                                
for x in max_stack:
    print x

# How many are alive now?

now = str(datetime.datetime.today())
print("\nThere are {0} laureates alive today (as of {1}):\n".format(len(living_stack),now[:10]))
surnames = [x.split(' ')[-1] for x in living_stack]
print(', '.join(surnames))

"""
import pandas as pd
from matplotlib import pyplot as plt

df = pd.DataFrame({'alive':_n,'dates':_d})
df.plot(x='dates',y='alive')
plt.show()
"""

print(min_alive)
print(min_latest_death)
print(min_stack)
