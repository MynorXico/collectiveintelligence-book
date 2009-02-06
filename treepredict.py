import collections

class decisionnode(object):
  def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
    self.col = col  # colum index of value to test
    self.value = value  # reference value
    self.results = results  # stores results in leafs, empty for inner nodes
    self.tb = tb  # child on true branch
    self.fb = fb  # child on false branch


def divideset(rows, column, value):
  split_function = None
  if isinstance(value, int) or isinstance(value, float):
    split_function = lambda row: row[column] >= value
  else:
    split_function = lambda row: row[column] == value
    
  # There has to be a `partition` or `group` function somewhere
  set1 = [row for row in rows if split_function(row)]
  set2 = [row for row in rows if not split_function(row)]
  return (set1, set2)


def uniquecounts(rows):
  results = collections.defaultdict(int)
  for row in rows:
    # Result is last column
    r = row[len(row) - 1]
    results[r] += 1
  return dict(results)


def giniimpurity(rows):
  """Returns probability that a randomly placed item will end up in the wrong
  category. A low result means that stuff is categorized well."""
  total = len(rows)
  counts = uniquecounts(rows)
  imp = 0
  # O(n^2) in number of categories
  for k1 in counts:
    p1 = float(counts[k1])/total  # XXX: These loops can be written more nicely
    for k2 in counts:
      if k1 == k2: continue
      p2 = float(counts[k2])/total
      imp += p1*p2
  return imp


def entropy(rows):
  from math import log
  log2 = lambda x: log(x)/log(2)
  results = uniquecounts(rows)
  ent = 0.0
  for r in results:
    p = float(results[r])/len(rows)
    ent -= p*log2(p)
  return ent


def buildtree(rows, scorefun=entropy):
  if len(rows) == 0: return decisionnode()
  current_score = scorefun(rows)

  best_gain = 0.0
  best_criteria = None
  best_sets = None

  column_count = len(rows[0]) - 1  # last column is result
  for col in range(0, column_count):
    # find different values in this column
    column_values = set([row[col] for row in rows])

    # for each possible value, try to divide on that value
    for value in column_values:
      set1, set2 = divideset(rows, col, value)

      # Information gain
      p = float(len(set1)) / len(rows)
      gain = current_score - p*scorefun(set1) - (1-p)*scorefun(set2)
      if gain > best_gain and len(set1) > 0 and len(set2) > 0:
        best_gain = gain
        best_criteria = (col, value)
        best_sets = (set1, set2)

  if best_gain > 0:
    trueBranch = buildtree(best_sets[0])
    falseBranch = buildtree(best_sets[1])
    return decisionnode(col=best_criteria[0], value=best_criteria[1],
        tb=trueBranch, fb=falseBranch)
  else:
    return decisionnode(results=uniquecounts(rows))


def printtree(tree, indent=''):
  if tree.results != None:  # leaf node
    print tree.results
  else:
    print '%s:%s?' % (tree.col, tree.value)

    print indent + 'T->',
    printtree(tree.tb, indent + '  ')
    print indent + 'F->',
    printtree(tree.fb, indent + '  ')


def testdata():
  def cleanup(s):
    s = s.strip()
    try:
      return int(s)
    except ValueError:
      return s
  return [map(cleanup, line.split('\t'))
      for line in open('decision_tree_example.txt')]


if __name__ == '__main__':

  tree = buildtree(testdata())
  printtree(tree)