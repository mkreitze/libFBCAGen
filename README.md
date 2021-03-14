# Preface

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

To generate, visualize and save FBCA, a variety of functions are used. They are sorted by dependence/relevence on one another, and their order is as follows:
initCA (FBCA initalization)
copyOver (Custom copying function for FBCA data structure)
updateFBCA (Updates FBCA once)

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
 **copyOver**
This function is made to copy over a level-map, which is a 2D array of cells, from one location in memeory to another. While a multitude of common copying methods already exist, when implemented the level-maps would fail to copy properly. To get around this, a custom functino was made. It is not efficient. 

```python
# Input: A list full of CACells
# Output: Another list full cells with the same states as the input
def copyOver(CAMapInit,length = FBCAConsts.CALength, width = FBCAConsts.CAWidth):
    CAMap=[]
    for x in range(0,length):
        holder=[]
        for y in range(0,width):
            holder.append(FBCAConsts.CACell())
            holder[y].state=CAMapInit[x][y].state
        CAMap.append(holder)
    return(CAMap)
```
**Example code**

```python
import FBCAConsts
import libFBCAGen

exFBCA1 = FBCAConsts.Fbca(); exFBCA2 = FBCAConsts.Fbca()
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}"); 
exFBCA1.levelMap = libFBCAGen.initCA(exFBCA1.levelMap,2,2)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}"); 
exFBCA2.levelMap = libFBCAGen.copyOver(exFBCA1.levelMap,2,2)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}"); 
```
Output: 
``` shell
1 -> []
2 -> []
1 -> [[<FBCAConsts.CACell object at 0x7f2aa1978208>, <FBCAConsts.CACell object at 0x7f2aa1978588>], [<FBCAConsts.CACell object at 0x7f2aa19785c0>, <FBCAConsts.CACell object at 0x7f2aa1978630>]]
2 -> [[<FBCAConsts.CACell object at 0x7f2aa1978208>, <FBCAConsts.CACell object at 0x7f2aa1978588>], [<FBCAConsts.CACell object at 0x7f2aa19785c0>, <FBCAConsts.CACell object at 0x7f2aa1978630>]]
1 -> [[<FBCAConsts.CACell object at 0x7f2aa1978208>, <FBCAConsts.CACell object at 0x7f2aa1978588>], [<FBCAConsts.CACell object at 0x7f2aa19785c0>, <FBCAConsts.CACell object at 0x7f2aa1978630>]]
2 -> [[<FBCAConsts.CACell object at 0x7f2aa1982128>, <FBCAConsts.CACell object at 0x7f2aa1982160>], [<FBCAConsts.CACell object at 0x7f2aa1982f60>, <FBCAConsts.CACell object at 0x7f2aa1982a20>]]
```

To better visualize the rest of the library, the rendering functions, and all associated functions are mentioned now. 

**makeFolder**
A function that generates a folder provided it doesnt already exist and the path is attinable. 
```python
### Input: Name of a folder we want to make
### Output: True (1) or False (0) if folder is made 
def makeFolder(folderName):
    try: 
        os.makedirs(folderName)
        return(1)
    except:
        return(0)
```
**Example code**
```python
import FBCAConsts
import libFBCAGen
d = f"{libFBCAGen.os.getcwd()}/test/"
libFBCAGen.makeFolder(d)
```
Output: 
A file named test appears in the same folder testCode.py is.

**colourConvert**
This is a simple switch function that returns a rgb tuple given an integer. The integer expected to be inputted in the state of a cell. For most applications, the first state is considered 'white space' in function of level-map generation, therefore changing this colour may yield nonsensical maps.
```python
### Input: state (as an int)
### Output: RGB touple
def colourConvert(x):
    return {
        0: (255,255,255),
        1: (0,0,0),
        2: (0,255,0),
        3: (0,0,255),
        4: (255,0,0),
        5: (51,255,255),
        6: (0,255,255),
        7: (255,69,0),
        8: (0,102,0),
        9: (153,0,153),
        10: (255,255,51),
    }[x]    
```

Due to this codes simplicity, no example code or output is shown.

**genIm**
genIm turns an FBCA into a visualized map. This is done through converting each state into a colour for a png image using colourConvert. To generate the image, the PIL library is used. 

```python
### Input: L_n (2d list of CACell with states), n, folder name, 
### Output: An image file
def genIm(CAMap,n=FBCAConsts.numOfStates,directory=os.getcwd(),quantifer="giveName"):
    im = Image.new('RGB', (n, n))
    for x in range(n):
        for y in range(n):
            im.putpixel((x,y),colourConvert(CAMap[x][y]))
    im.save(f"{directory}{quantifer} {str(n)}.png")
    return(im)

```
**Example code**
```python
def genIm(CAMap,length = FBCAConsts.CALength-1, width = FBCAConsts.CAWidth-1 , directory = os.getcwd(),quantifer="/", gen = 0):
    im = Image.new('RGB', (length, width))
    for x in range(length):
        for y in range(width):
            im.putpixel((x,y),colourConvert(CAMap[x][y].state))
    im.save(f"{directory}{quantifer} {str(gen)}.png")
    return(im)
```
Output: 
The following image is saved into the current working directory [L_0](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/0.png)

**updateMap**
Update Map takes an existing FBCA and goes through one discrete time step. The updating function is mathematicall defined as, [this hard to read thing](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/update%20function.png). In more common terms, a cell takes the state of its highest scoring neighbour. The neighbourhood of a cell is represented by a list of tuples. For example: [(-1,0) , (1,0) , (0,-1) , (0,1)] is a neighbourhood that represents the above, below, left and right cells of a given cell (called the von Neumann neighbourhood of a cell).  

**Example code**


Output: 

**initCA**
**Example code**
**initCA**
**Example code**
**initCA**
**Example code**
**initCA**
**Example code**
