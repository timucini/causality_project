# Causality checking using machine learning
## Variables
| Variable | Description |
| --- | --- |
| t | time |
| c | costs |
| x | generic features |
| n | particular change |
| d<sub>n</sub> | feature of a change |
| p | &sum;(n) representing the process &rarr; e{0;1} |
## Assumption
t(x) = f<sub>t</sub>(x) + g<sub>t</sub>(p)</br>
c(x) = f<sub>c</sub>(x) + g<sub>c</sub>(p)</br>
using c as generic:</br>
g(p) = &sum;(d<sub>n</sub>)
## Procedure
c<sub>p=0</sub> = m<sub>p=0</sub>(x)</br>
c<sub>p=1</sub> = m<sub>p=1</sub>(x)</br>
&Delta;<sub>c</sub> = c<sub>p=0</sub> - c<sub>p=1</sub></br>
causality &equiv; accuracy(m<sub>c</sub>(g(1))&rarr;&Delta;<sub>c</sub>)