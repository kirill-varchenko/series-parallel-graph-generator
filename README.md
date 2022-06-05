# series-parallel-graph-generator

Python implementation of the algorithm described in [Yukinao Isokawa, Series-parallel circuits and continued fractions](http://dx.doi.org/10.12988/ams.2016.63103). String representation of series-parallel circuits is preserved.

Sample output:
```
n=1
     r
total=1

n=2
     (s r r)
     (p r r)
total=2

n=3
     (s r r r)
     (s r (p r r))
     (p r r r)
     (p r (s r r))
total=4

n=4
     (s r r r r)
     (s r r (p r r))
     (s (p r r) (p r r))
     (s r (p r r r))
     (s r (p r (s r r)))
     (p r r r r)
     (p r r (s r r))
     (p (s r r) (s r r))
     (p r (s r r r))
     (p r (s r (p r r)))
total=10
```