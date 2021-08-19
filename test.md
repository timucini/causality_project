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
The first assumptions that need to be made are those that represent the KPI's. In this case, these are `c` and `t`. So we can assume that the result is calculated by a function `f` which takes the generic characteristics `x` as input. In addition, the result changes due to the changes `p` made. This is achieved by adding the function `g` which uses `p` as input.</br> 
t(x) = f<sub>t</sub>(x) + g<sub>t</sub>(p)</br>
c(x) = f<sub>c</sub>(x) + g<sub>c</sub>(p)</br>
Using the example `c`, it must be explained for the next assumptions that the result does not change if the process is not changed.</br>
g(0) = 0</br>
However, on the other hand, it is true that the function `g` is the sum of all the functions of the changes of the process.</br>
g(p) = &sum;(d<sub>n</sub>)
## Procedure
In order to prove causality, it is necessary to define the actual results as predictions of a model `m`.</br>
c<sub>p=0</sub> = m<sub>p=0</sub>(x)</br>
In the next step it is necessary to determine the difference &Delta; between the prediction of the model and the results of the changed process c<sub>p=1</sub>. This represents the change in the KPI that resulted from the change in the process.</br>
&Delta;<sub>c</sub> = c<sub>p=0</sub> - c<sub>p=1</sub></br>
Finally, another model `M` is used to try to determine the change in KPI based on the changes `g(1)`. The better this succeeds, i.e. the higher this accuracy is, the more one can speak of a causal relationship.</br>
causality &equiv; accuracy(M<sub>c</sub>(g(1))&rarr;&Delta;<sub>c</sub>)</br>
In addition, under the following assumption, each individual change can also be checked.</br>
causality &equiv; &sum;<sup>n</sup>accuracy(M<sub>c<sub>n</sub></sub>(d(n))&rarr;&Delta;<sub>c<sub>n</sub></sub>)

Sources:</br>
https://link.springer.com/article/10.1365/s40702-019-00557-y </br>
https://ichi.pro/de/1-1-bessere-entscheidungsfindung-wenn-kausale-folgerung-auf-maschinelles-lernen-trifft-208061114886251