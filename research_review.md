### Research review: Game Tree Searching by min / max approximation _by Ronald L. Rivest, MIT_ 

This paper introduces penalty based technique for game tree searching that by approximating min and max operators with mean-valued operators guides the selection of leaf that should be expanded - it selects leafs upon which values root value depends the most. This is achieved by calculating derivatives of generalized mean value function at each node and applying the chain rule. 

##### A brief summary of techniques introduced

A generalized _p-mean_ of __a__, denoted as $M_{p}$ is just a _p-th_ root of the sum of elements of __a__ to the _p-th_ power devided by the number of elements of __a__. For the purposes of the techniques introduced we are most interested in the fact that

$$
\lim_{p \to \infty} M_{p}(\boldsymbol a) = max(a_{1}, ... , a_{n});
\lim_{p \to -\infty} M_{p}(\boldsymbol a) = min(a_{1}, ... , a_{n})
$$

Which in plain words mean that for low values of $p$ this function is good approximation of minimum value and for high values of $p$ it is good approximation of maximum values with one added benefit - this function is diferentiable with a partial derivative with respect to $a_{i}$ given by

$\frac{\partial M_{p}(\boldsymbol a)}{\partial a_{i}} = \frac{1}{n} \bigg( \frac{a_{i}}{M_{p}(\boldsymbol a)} \bigg)^{p-1}$

One of the main ideas from this article is that by using generalized mean values to approximate _min_ and _max_ functions and by taking derivative at each node of the tree we can idendify the node upon which value of the root depends the most via chain rule. We would expend that node next.

##### A brief summary of results achieved

Authors compare their proposed technique to the _minimax search with alpha-beta pruning_ for the game of _Connect-Four_. They eveluate these two  techniques first by limiting time per turn (CPU time) and then by limiting moves the algorithm considers. When CPU time is the limiting factor _minimax search with alpha-beta pruning_ seems to be the better choice - total wins:losses:ties  186:239:65. However if the limit factor is changed to the number of moves the algorithm can make, then the situation is revered and _minimax approximation_ technique acheives better results - total wins:losses:ties  249:190:51. Authors noticed that when CPU time was limited, _alpha-beta pruning_ considered three times more distince positions than _minimax approximation_ technique.

---
Prepared by Vaidas Armonas as part of Isolation Project submision for Artificial Intelligence ND.