# Preface

Fashion Based Cellular Automata (FBCA) are self organizing structures that are normal cellular automata with a governing rule set known as a score matrix. This score matrix allows a single cell of a FBCA to change its state to a nearby more desirable state by evaluating scores assigned to each cell. FBCAs have been found to be extremely useful for level-map genreation in videogames. This comes from an FBCA exhibiting local self organizing behaviour which, when paired with an inital random state, produce level-maps that have similar local behaviour but different overall configurations. FBCA were first defined (here). For a more applied explination the map below has been generated using FBCA.

![A cavern map image](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/niceImage%206.png)

With one or two applications of paintbucket tool in paint, we obtain: 

![A nice level-map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/niceImage%20recolour.png)
The above map could easily represent a cavern system full of water (represented by blue), open caves (represented by white), some dangerous material (represented by red) and valuable ore (represented by black) and exceedingly rare ore (reprsented by green and dark blue). The beneifit of FBCA if their abiltiy to reproduce local behaviour. Simply changing the inital random state, we get the following similar maps, each taking a few seconds to generate:

![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand1%20recolour.png)
![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand2%20recolour.png)
![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand1%20recolour.png)

The following is the library that allows for easy generation and saving of FBCA for level-map generation. 

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
It should be noted that the 'connectivity' described by F is too arbtirary to generate efficent code for. To get around this, F is considered by default to be a torus of 100 cells in width and 100 cells in length with each cell connected to its first degree Von Neumann neighbour. Note: the neighbourhood of a cell is represented by a list of tuples. For example: [(-1,0) , (1,0) , (0,-1) , (0,1)] is a neighbourhood that represents the above, below, left and right cells of a given cell (called the von Neumann neighbourhood of a cell).  

Additionally, L_0 has not been defined yet as we need to define the data structures for cells and FBCA as well as a generating function.

# FBCA representation  (FBCAConsts.py)

As mentioned earlier, FBCA have five defining features. While these five defining features are required to specify a FBCA, it is also useful to know what the FBCA ends up as. This is represented by its L_g (more commonly known as its final image or _resulting level-map_). These levelmaps are usually classified into different 'behaviours' leading to a quantity known as behaviourNum to record which behaviour a level-map is similar to. This leads to the following data structure being used to define a FBCA. 

```python
# FBCA data structure #
class Fbca:
    levelMap=[] # L_g
    scoreMatrix=[] # S
    behaviourNum=0 # iso-behavioural identification 
    g = numOfGens
    n = numOfStates
    neighbourhood = neighbours
    torusWidth = CAWidth
    torusLength = CALength
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
The first function is the generation of an FBCAs inital conditions, known as its L_0. This is done through use of rand.randint to populate each cell with state from 0 to n-1. This leads to the standard representation of a level-map. Level-maps are a grid of states, represented by a 2D list, saved row wise. This method is preferred to standard methods, as the representation for fbcas/cells does not do well with standard copying functions. 

```python
# Input: An FBCA 
# Output: A level-map pseudo-random collection of states
def initCA(fbca):
    #Fills in downward stripes as we interate x then y
    for x in range(0,fbca.torusLength):
        holder=[] #downward column at the x value
        for y in range(0,fbca.torusWidth):
            holder.append(FBCAConsts.CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,FBCAConsts.numOfStates-1)
        fbca.levelMap.append(holder)
    return(fbca.levelMap)
```
**Example code**
From initCA.py
```python
import FBCAConsts
import libFBCAGen

exFBCA = FBCAConsts.Fbca()
exFBCA.torusLength = 2; exFBCA.torusWidth = 2
print (f"1 -> {exFBCA.levelMap}")
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
print (f"1 -> {exFBCA.levelMap}")
```
output: 
```shell
1 -> []
[[<FBCAConsts.CACell object at 0x7f02f51d4730>, <FBCAConsts.CACell object at 0x7f02f50fefa0>], [<FBCAConsts.CACell object at 0x7f02f50fe850>, <FBCAConsts.CACell object at 0x7f02f50b4700>]]
```
 **copyOver**
This function is made to copy over a level-map, which is a 2D array of cells, from one location in memeory to another. While a multitude of common copying methods already exist, when implemented the level-maps would fail to copy properly. To get around this, a custom function was made. It is not efficient. 

```python
# Input: A list full of CACells
# Output: Another list full cells with the same states as the input
def copyOver(fbca):
    CAMap=[]
    for x in range(0,fbca.torusLength):
        holder=[]
        for y in range(0,fbca.torusWidth):
            holder.append(FBCAConsts.CACell())
            holder[y].state=fbca.levelMap[x][y].state
        CAMap.append(holder)
    return(CAMap)
```
**Example code**

```python
import FBCAConsts
import libFBCAGen

exFBCA1 = FBCAConsts.Fbca()
exFBCA1.torusLength = 2; exFBCA1.torusWidth = 2
exFBCA2 = FBCAConsts.Fbca(); exFBCA2.levelMap = []
exFBCA2.torusLength = 2; exFBCA2.torusWidth = 2
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")
exFBCA1.levelMap = libFBCAGen.initCA(exFBCA1)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")
exFBCA2.levelMap = libFBCAGen.copyOver(exFBCA1)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")
```
Output: 
``` shell
1 -> []
2 -> []
1 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54730>, <FBCAConsts.CACell object at 0x7fcf7cd45850>], [<FBCAConsts.CACell object at 0x7fcf7cd457f0>, <FBCAConsts.CACell object at 0x7fcf7ccd11f0>]]
2 -> []
1 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54730>, <FBCAConsts.CACell object at 0x7fcf7cd45850>], [<FBCAConsts.CACell object at 0x7fcf7cd457f0>, <FBCAConsts.CACell object at 0x7fcf7ccd11f0>]]
2 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54520>, <FBCAConsts.CACell object at 0x7fcf7ccd1fa0>], [<FBCAConsts.CACell object at 0x7fcf7ccd16a0>, <FBCAConsts.CACell object at 0x7fcf7ccf22b0>]]
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
This is a simple switch function that returns a RGB tuple given an integer. The integer expected to be inputted in the state of a cell. For most applications, the first state is considered 'white space' in function of level-map generation, therefore changing this colour may yield nonsensical maps.
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
### Input: A FBCA, folder name, quantifer
### Output: An image file
def genIm(fBCA, directory = os.getcwd(),quantifer="", gen = 0):
    im = Image.new('RGB', (fBCA.torusLength, fBCA.torusWidth))
    for x in range(fBCA.torusLength):
        for y in range(fBCA.torusWidth):
            im.putpixel((x,y),colourConvert(fBCA.levelMap[x][y].state))
    im.save(f"{directory}/{quantifer} {str(gen)}.png")
    return(im)
```

**Example code**
```python
import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
libFBCAGen.genIm(exFBCA,quantifer = "/genIm")
```
Output: 
The following image is saved into the current working directory

![L_0](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/genIm%200.png)

**updateMap**
updateMap takes an existing FBCA and goes through one discrete time step. The updating function is mathematicall defined as, [this hard to read thing](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/update%20function.png). In more common terms, a cell takes the state of its highest scoring neighbour. The updating function occurs in three steps, first each score is determined. Then the levelmap is copied. The original levelmap is searched for highest scoring neighbours and states of the copied map are changed. This updated copy is then returned.

```python
# Input: FBCA to update
# Output: L_(n+1) (2d list of CACells)
def updateMap(fbca):

    for x in range(0,fbca.torusLength):
        for y in range(0,fbca.torusWidth):
            #Need to get score from center square and its neighbours.
            row = fbca.levelMap[x][y].state*fbca.n #the center colour determines the row of the score matrix used 
            #new method to save a small amount of computation
            col0=fbca.levelMap[(x+fbca.neighbourhood[0][0])%fbca.torusLength][(y+fbca.neighbourhood[0][1])%fbca.torusWidth].state 
            col1=fbca.levelMap[(x+fbca.neighbourhood[1][0])%fbca.torusLength][(y+fbca.neighbourhood[1][1])%fbca.torusWidth].state 
            col2=fbca.levelMap[(x+fbca.neighbourhood[2][0])%fbca.torusLength][(y+fbca.neighbourhood[2][1])%fbca.torusWidth].state 
            col3=fbca.levelMap[(x+fbca.neighbourhood[3][0])%fbca.torusLength][(y+fbca.neighbourhood[3][1])%fbca.torusWidth].state
            fbca.levelMap[x][y].score=fbca.scoreMatrix[row+col0]+fbca.scoreMatrix[row+col1]+fbca.scoreMatrix[row+col2]+fbca.scoreMatrix[row+col3]
    #start by copying the map
    CAMapCopy=copyOver(fbca)
    #for every cell, find the highest score among neighbours
    for x in range(0,fbca.torusLength):
        for y in range(0,fbca.torusWidth):
            #NOTE: We give priority to the center square on ties. Priority continues up with the last defined neighbour to have the worst priority
            bigScore=0;bigScore=fbca.levelMap[x][y].score
            #compares neighbours scores, reassigning bigScore and state if someone is bigger
            for z in fbca.neighbourhood:
                if(bigScore<fbca.levelMap[(x+z[0])%fbca.torusLength][(y+z[1])%fbca.torusWidth].score):
                    bigScore=fbca.levelMap[(x+z[0])%fbca.torusLength][(y+z[1])%fbca.torusWidth].score
                    CAMapCopy[x][y].state=fbca.levelMap[(x+z[0])%fbca.torusLength][(y+z[1])%fbca.torusWidth].state
    return(CAMapCopy)
```

**Example code**
``` python 
import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA.levelMap)
totalNumOfGens = 5
for n in range(totalNumOfGens):
    libFBCAGen.genIm(exFBCA,gen = n)
    exFBCA.levelMap = libFBCAGen.updateMap(exFBCA)
```

Output: 
The following level-map visualizations are produced: 

![L0](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/updateMap%200.png)
![L1](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/updateMap%201.png)
![L2](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/updateMap%202.png)
![L3](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/updateMap%203.png)
![L4](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/updateMap%204.png)

**genText**
Saves an FBCA into a text document. This is done by first (optionally) saving the cells of the FBCA as a string of integers representing each cells state. The following string;

sMs{fbca.scoreMatrix}g{fbca.g}n{fbca.n}w{fbca.torusWidth}l{fbca.torusLength}neighbours{fbca.neighbourhood}

then records the g (updates), n (number of states), torus width, torus length and each cells neighbourhood.

``` python 
# saves fbca in a text doc
# Input: FBCA, directory, fileName, newFile, justMap
def genText(fbca, directory = os.getcwd(), fileName = "test.txt", newFile = True, justMap = False):
    if newFile == True: 
        f = open(fileName, "w")
    else:
        f = open(fileName, "a")
    for x in range(fbca.torusWidth):
        for y in range(fbca.torusLength):
            f.write(f"{fbca.levelMap[x][y].state}")
    f.write("\n")
    if justMap == False:
        f.write(f"sMs{fbca.scoreMatrix}g{fbca.g}n{fbca.n}w{fbca.torusWidth}l{fbca.torusLength}neighbours{fbca.neighbourhood}\n")
    return()
```
**Example code**
```python
import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
exFBCA.g = 6
libFBCAGen.genText(exFBCA,fileName = "genTextExample.txt")
```
Output: 
The following text file. 

**generateFBCA**
This function takes a _assumed to be initalized_ FBCA and fully generates it. It allows for each frame of the FBCA to be saved as a png image coloured coded by colourConvert or saved as a string of integers onto a textfile using genText.  
```python
# Input: fbca, directory, quantifer
# Output: L_g for the system, if saved, L will be generated in as folder named by the quantifer.
def generateFBCA(fbca,directory = os.getcwd(),quantifer = "test", saveImages = False, saveFinalImage = False):
    gif=[];CAMap=[];CAMap=copyOver(fbca) #PIL shenningans
    if (saveImages == True ) or (saveFinalImage == True ):
        directory=f"{directory}/{quantifer}/"
    makeFolder(directory)
    for n in range(fbca.g):
        if (saveImages == True):
            gif.append(genIm(fbca, directory, quantifer, gen = n))
        fbca.levelMap=updateMap(fbca)
    if (saveFinalImage==1):
        gif.append(genIm(fbca, directory, quantifer, fbca.g))
        gif[0].save(f"{directory}{quantifer}.gif",save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    return(CAMap)
```
**Example code**
```python
import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
exFBCA.g = 6
exFBCA.levelMap = libFBCAGen.generateFBCA(exFBCA,saveFinalImage=True, saveImages= True, saveFinalText = True, quantifer = "generateFBCAExample")
```
Output:
The folder :


