# Preface

Fashion Based Cellular Automata (FBCA) are self organizing structures that are normal cellular automata with a governing rule set. This rule set allows a single cell of a FBCA to change its state to a nearby more desirable state by evaluating scores assigned to each cell. FBCAs have been found to be extremely useful for level-map genreation in videogames. This comes from an FBCA exhibiting local self organizing behaviour which, when paired with an inital random state, produce level-maps that have similar local behaviour but different overall configurations. 

# put example image here.

# Initalizations
To properly define a FBCA, five parameters are required. As shown in (thesis plug), these parameters are: 
- F -> connectivity of each cell in the FBCA (its neighbourhood).
- g -> the number of updates done to an FBCA before completion 
- n -> number of states in the FBCA 
- S -> the score matrix
- L_0 -> the inital random set of states

For a 'default' FBCA the following parameters are used:
```python
CALength=100  # (F)
CAWidth=100 # (F)
neighbours=[] # (F)
neighbours.append((0,1)) # (F)
neighbours.append((0,-1)) # (F)
neighbours.append((-1,0)) # (F)
neighbours.append((1,0)) # (F)
numOfGens=40 # (g)
numOfStates=2 # (n)
scoreMatrix = [1,2,3,4] # (S)
```
It should be noted that the 'connectivity' described by F is too arbtirary to generate efficent code for. To get around this, F is considered by default to be a torus of 100 cells in width and 100 cells in length with each cell connected to its first degree Von Neumann neighbour. 

Additionally, L_0 has not been defined yet as we need to define the data structres that represent cells and FBCA.

# FBCA represntation
class CACell:
    state=0
    score=0

# FBCA data structure #

As mentioned earlier, FBCA have five defining features. While these five defining features are required to specify a FBCA, it is also useful to know what the FBCA ends up as. This is represented by its L_g (more commonly known as its final image or _resulting level-map_). These levelmaps are usually classified into different 'behaviours' leading to a quantity known as behaviourNum to record which behaviour a level-map is similar to. This leads to the following data structure being used to define a FBCA. 

```python
class Fbca:
    levelMap=[]
    scoreMatrix=[]
    behaviourNum=0
    g = numOfGens
    n = numOfStates
    neighbourhood = neighbours
    torusWidth = CAWidth
    torusLength = CALength
```
It should be noted that the final 5 parameters are almost always considered to be globally defined and are usually commented out to reduce computation times.

