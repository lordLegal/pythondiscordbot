import tt
import re
from stackapi import StackAPI


SITE = StackAPI('stackoverflow')
# questions = SITE.fetch('questions', max=10,
#                       min=10, tagged='test test', sort='votes')
questions = SITE.fetch('questions', max=10, tagged='python', sort='votes')
a = str(questions)
c = questions['backoff']

g1 = re.sub("'", "", a)
g2 = re.sub("{", "", g1)
g3 = re.sub("}", "", g2)
g4 = re.sub(":", "", g3)
g5 = re.sub(",", "", g4)

l = tt.Find(a)
print(l)
