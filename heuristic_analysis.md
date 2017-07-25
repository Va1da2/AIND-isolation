# Custom Heuristics considered

For this task I have considered many different variantions of standard heuristics (player open moves vs. opponent open moves and different combinations) and some less stright forward ones. The heuristics that I kept are:

* custom_score_3: squared distance between players. The rationel for this metric is to take into account how far appart palyers are from each other. This might indicate how much space they have for them selves. On its own, this is not a great heuristic but it contributes to the combined score quite well.
* custom_score_2: variant of players moves and opponents moves score. I figured that scaling how much we value number of remaining moves to the player vs. number of remaining moves to the opponent should depend on the stage of the game, which I approximated by the number of blanck spaces on the board divided by the number of blocked spaces. In this way we will put more emphasis on the number of oponent moves left the more game progresses. 
* custom_score: mains score is a combination of the above two scores: 25% of custom_score_3 and 75% custom_score_2. This is just an experimental results of trying different setups. Since results of the _tournament.py_ exibit high variance this is also might be not the best setup - just the best that happened during my testing.

# Resutls of the _tournament_

```
                        *************************                         
                             Playing Matches                              
                        *************************                         

 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3 
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost 
    1       Random       8  |   2     9  |   1     7  |   3     8  |   2  
    2       MM_Open      3  |   7     6  |   4     4  |   6     6  |   4  
    3      MM_Center     5  |   5     7  |   3     3  |   7     6  |   4  
    4     MM_Improved    1  |   9     5  |   5     2  |   8     5  |   5  
    5       AB_Open      5  |   5     7  |   3     8  |   2     4  |   6  
    6      AB_Center     6  |   4     5  |   5     3  |   7     5  |   5  
    7     AB_Improved    4  |   6     4  |   6     4  |   6     3  |   7  
--------------------------------------------------------------------------
           Win Rate:      45.7%        61.4%        44.3%        52.9%   
```

Results indicate that the proposed _AB\_Custom_ agent beets its oponents on overall win rate. It also performs at least as good or better when put agains _MM\_Improved_ or _AB\_Improved_. It outscores _AB\_Improved_ by more than __15 percentage points__ (a third of _AB\_Improved_ win rate). 
The other point to note is that both _AB\_Custom_2_ and _AB\_Custom_3_ has a lower win rate than our chosen _AB\_Custom_. In particular _AB\_Custom_2_ has even lower win rate than _AB\_Improved_, however when combined together  they produce a superior results - this is a model ansamble effect. By combining several week models we have a good perfoming model.

Another ilustration of _AB\_Custom_ supperiority is the average win rate over several runs of the tournament. I made 5 runs of the tournament and win rates for all the heuristics presented bellow

![graphs_of_average_win_rate](/Users/vaidasarmonas/Documents/Udacity/AIND/AIND-Isolation/tournament_runs_bar_chart.jpeg)

As can be seen from the graph - the _AB\_Custom_ heuristic performs just a little bit better on average than the rest. In fact it has at least 6 percentage points advantage over the other scores on average (The average percentages are 52%, 58%, 52% and 49% respectively).

Based on the above I would suggest to use the _AB\_Custom_ heuristic as the optimal score function:

* it is the most performant of the all considered heuristics;
* it combines two simpler and very different heuristics into one;
* it is still quite simple and therefore fast to compute.
 
These results are still very run dependent and a lot more investigation. Next steps would be to consider event more simple heuristics with very different interpretations and see what result we can achieve by combining them in different way.


---
Prepared by Vaidas Armonas as part of Isolation Project submision for Artificial Intelligence ND.