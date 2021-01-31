# # Preface

Fashion Based Cellular Automata (FBCA) are self organizing structures that are normal cellular automata with a governing rule set known as a score matrix. This score matrix allows a single cell of a FBCA to change its state to a nearby more desirable state by evaluating scores assigned to each cell. FBCAs have been found to be extremely useful for level-map genreation in videogames. This comes from an FBCA exhibiting local self organizing behaviour which, when paired with an inital random state, produce level-maps that have similar local behaviour but different overall configurations. FBCA were first defined (here). 

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

Additionally, L_0 has not been defined yet as we need to define the data structures for cells and FBCA as well as a generating function.

# FBCA representation  (FBCAConsts.py)

As mentioned earlier, FBCA have five defining features. While these five defining features are required to specify a FBCA, it is also useful to know what the FBCA ends up as. This is represented by its L_g (more commonly known as its final image or _resulting level-map_). These levelmaps are usually classified into different 'behaviours' leading to a quantity known as behaviourNum to record which behaviour a level-map is similar to. This leads to the following data structure being used to define a FBCA. 

```python
# FBCA data structure #
class Fbca:
    levelMap=[] # L_g
    scoreMatrix=[] # S
    behaviourNum=0 # iso-behavioural identification 
    # g = numOfGens
    # n = numOfStates
    # neighbourhood = neighbours
    # torusWidth = CAWidth
    # torusLength = CALength
```
It should be noted that the final 5 parameters are almost always considered to be globally defined and are usually commented out to reduce computation times.

Each cell of a FBCA requires also requires a data structure to store its score and current state, as shown below. 

```python
class CACell:
    state=0
    score=0
```

These data structures are used for most work with FBCAs and are contained within the file FBCAConsts.py and must be imported. Now that we have defined our data structures and global constants, we can start defining functions.

# Functions

 **initCA**
The first function is the generation of an FBCAs inital conditions, known as its L_0. This is done through use of rand.randint to populate each cell with state from 0 to n-1. This leads to the standard representation of a level-map. Level-maps are a grid of states, represented by a 2D list, saved row wise.

```python
# Input: A list full of CACells (representing an empty FBCA)
# Output: A list full of CACells with a pseudo-random collection of states
def initCA(CAMap,length = FBCAConsts.CALength, width = FBCAConsts.CAWidth):
    #Fills in downward stripes as we interate x then y
    for x in range(0,length):
        holder=[] #downward column at the x value
        for y in range(0,width):
            holder.append(FBCAConsts.CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,FBCAConsts.numOfStates-1)
        CAMap.append(holder)
    return(CAMap)
```
**Example code**
From initCA.py
```python
import FBCAConsts
import libFBCAGen

exFBCA = FBCAConsts.Fbca()
print (f"1 -> {exFBCA.levelMap}")
exFBCA.levelMap = libFBCAGen.initCA(exFBCA.levelMap,2,2)
print (exFBCA.levelMap)
```
output: 
```shell
1 -> []
[[<FBCAConsts.CACell object at 0x7fa3a4168080>, <FBCAConsts.CACell object at 0x7fa3a418b828>], [<FBCAConsts.CACell object at 0x7fa3a418ba90>, <FBCAConsts.CACell object at 0x7fa3a418bac8>]]
```
 **initCA**
**Example code**
 **initCA**
**Example code**
**initCA**
**Example code**
