import json
from urllib2 import urlopen

created = []
closed = []

page = 1
while True:
    c = json.load(urlopen('https://api.github.com/repos/astropy/astropy/issues?state=closed&per_page=100&page={page}'.format(page=page)))
    for i in c:
        created.append(i['created_at'])
        closed.append(i['closed_at'])
    if len(c) == 0:
        break
    page += 1

page = 1
while True:
    o = json.load(urlopen('https://api.github.com/repos/astropy/astropy/issues?state=open&per_page=100&page={page}'.format(page=page)))
    for i in o:
        created.append(i['created_at'])
    if len(o) == 0:
        break
    page += 1
    
f = open('created.txt', 'w')
for c in created:
    f.write(c + '\n')
f.close()

f = open('closed.txt', 'w')
for c in closed:
    f.write(c + '\n')
f.close()

# so=set([i['number'] for i in o])
# sc=set([i['number'] for i in c])
# so.intersection(sc)
