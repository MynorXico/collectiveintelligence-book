import collections
import time
import random
import math

def getminutes(t):
  x = time.strptime(t, '%H:%M')
  return x[3]*60 + x[4]


def printschedule(r, dest):
  for d in range(len(r)/2):
    name = people[d][0]
    origin = people[d][1]
    out = flights[(origin, dest)][r[d]]
    ret = flights[(origin, dest)][r[d + 1]]
    print '%10s%10s %5s-%5s %3s %5s-%5s $%3s' % (
        name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])


def costfunc(flights, dest):
  def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60

    for d in range(len(sol)/2):
      origin = people[d][1]
      outbound = flights[(origin, dest)][int(sol[d])]
      returnf = flights[(dest, origin)][int(sol[d+1])]

      totalprice += outbound[2] + returnf[2]

      latestarrival = max(latestarrival, getminutes(outbound[1]))
      earliestdep = min(latestarrival, getminutes(returnf[0]))

    # Every person must wait until the last person arrives.
    # They must also arrive when the first flight leaves
    totalwait = 0
    for d in range(len(sol)/2):
      origin = people[d][1]
      outbound = flights[(origin, dest)][int(sol[d])]
      returnf = flights[(dest, origin)][int(sol[d+1])]
      totalwait += latestarrival - getminutes(outbound[1])
      totalwait += getminutes(returnf[0]) - earliestdep

    # One additional day of car rental fees?
    if latestarrival >= earliestdep: totalprice += 50

    return totalprice + totalwait
  return schedulecost


def randomoptimize(domain, costf):
  best = 99999999
  bestr = None
  for i in range(1000):
    r = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
    cost = costf(r)
    if cost < best:
      best = cost
      bestr = r
  return r

if __name__ == '__main__':
  people = [
      ('Seymour', 'BOS'),
      ('Franny', 'DAL'),
      ('Zooey', 'CAK'),
      ('Walt', 'MIA'),
      ('Buddy', 'ORD'),
      ('Les', 'OMA'),
      ]

  destination = 'LGA'  # LaGuardia (New York)

  flights = collections.defaultdict(list)

  for line in open('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights[(origin, dest)].append( (depart, arrive, int(price)) )

  f = costfunc(flights, destination)
  domain = [(0, 8)] * (len(people) * 2)

  r = randomoptimize(domain, f)
  printschedule(r, destination)
  print f(r)