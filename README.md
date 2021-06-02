# How to use

The following libraries are required to use this library for map generation: 

Python 3<br />
PIL (python image library)<br />
os (operating system library)<br />
time <br />
random <br />

To use, simply download **FBCAConsts.py** and **libFBCAGen.py** to your working directory. From here use normal import commands to access any functions and data structures. Within this git (as well as in this readme) there are a variety of example codes. Below is preface of what this package can do.

# Preface

The following is a quick, reproducible and infinitely scalable method to generate similar looking videogame level-maps using fashion based cellular automata. Fashion Based Cellular Automata (FBCA) are self organizing structures that are normal cellular automata with a governing rule set known as a score matrix. This score matrix allows a single cell of a FBCA to change its state to a nearby more desirable state by evaluating scores assigned to each cell. Since FBCA exhibit self organizing behaviour which, when they are paired with an initial random state they produce level-maps that have similar local behaviour but different global configurations. FBCA were first defined (here). As a visual, the image below is made by an FBCA. 

![A cavern map image](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/niceImage%206.png)

With one or two applications of paintbucket tool in paint, we obtain: 

![A nice level-map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/niceImage%20recolour.png)

The above map could easily represent a cavern system full of water (represented by blue), open caves (represented by white), some dangerous material (represented by red), valuable ore (represented by black) and exceedingly rare ore (represented by green and dark blue). The meaning of each colour in any FBCA is up to the user. The benefit of FBCA if their ability to reproduce local behaviour. Simply changing the initial random state, we get the following similar maps. It should be noted that map takes only a few seconds to generate:

![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand1%20recolour.png)
![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand2%20recolour.png)
![Another nice map](https://github.com/mkreitze/libFBCAGen/blob/master/resources/niceImage/rand1%20recolour.png)

The following is the library that allows for easy generation and saving of FBCA for level-map generation. It starts by showing FBCAConsts.py, the 'header file' that defines the data structure and default parameters. The library functions (with examples) are shown later.

# Initializations
To properly define a FBCA, five parameters are required. As shown [here](https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316), these parameters are: 

- F -> connectivity of each cell in the FBCA (its neighbourhood)<br />
- g -> the number of updates done to an FBCA before completion<br />
- n -> number of states in the FBCA<br />
- S -> the score matrix<br />
- L_0 -> the initial random set of states<br />

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
It should be noted that the 'connectivity' described by F is too arbitrary to generate efficient code for. To get around this a user can specify the neighbourhood via a list of tuples. Each tuple is the (x,y) offset from the current cell. For example (0,-1) is one below. The neighbourhood is defaulted to its von Neumann neighbourhood: [(-1,0) , (1,0) , (0,-1) , (0,1)] (the cells one above, below, left and right of a cell). 

One might notice L_0 this is due to a lack of data structures and a 'random' generating function.

# FBCA representation  (FBCAConsts.py)

All five previously mentioned parameters are defined as well as L_g. L_g represents what the FBCA looks like after all of its updates are completed. When first initialized L_g (more commonly known as its final image or _resulting level-map_) is L_0. Behaviour number is used for analysis of FBCAs which is done by this library [libGenAna](https://github.com/mkreitze/libFBCAAna). Thus FBCAs have the following data structure.

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

Each cell of a FBCA requires also requires a data structure to store its score and current state, this is the simple data structure shown below. 

```python
class CACell:
    state=0
    score=0
```

These data structures are used for most work with FBCAs and are contained within the file FBCAConsts.py and must be imported. Now that we have defined our data structures and global constants, we can start defining functions.

# Functions
The functions are in the following order: 

initCA (FBCA initialization)<br />
copyOver (Custom copying function for FBCA data structure)<br />
makeFolder<br />
colorConvert<br />
genIm (image visualization for FBCA)<br />
updateFBCA (Updates FBCA once)<br />
genText (text record for FBCA)<br />
generateFBCA (fully generates parameterized FBCA)<br />

# initCA

This function fills a FBCA's level-map with states initialized using random's randint function. 

**Example call:**

fbca.levelMap = initCA(fbca) 

**Arguments:**

*fbca*: An initialized FBCA data structure. It does not have to be filled with anything. 

**Outputs:**

*fbca.levelMap*: A level-map full of random states. 

**Example (initCAExample.py)**
```python
import FBCAConsts
import libFBCAGen

exFBCA = FBCAConsts.Fbca()
exFBCA.torusLength = 2; exFBCA.torusWidth = 2
print (f"1 -> {exFBCA.levelMap}")
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
print (f"1 -> {exFBCA.levelMap}")
```

**Example Output:** 
```shell
1 -> []
[[<FBCAConsts.CACell object at 0x7f02f51d4730>, <FBCAConsts.CACell object at 0x7f02f50fefa0>], [<FBCAConsts.CACell object at 0x7f02f50fe850>, <FBCAConsts.CACell object at 0x7f02f50b4700>]]
```

# copyOver

This function is made to copy over a level-map, which is a 2D array of cells, from one location in memory to another. While a multitude of common copying methods already exist, when implemented the level-maps would fail to copy properly. To get around this, a custom function was made. It is not efficient. 

**Example call:**

fbca2.levelMap = copyOver(fbca1)

**Arguments:**

*fbca*: An FBCA whose cellular automata has been initialized with states.  

**Output:**

*CAMap*: A new data structure containing the same level-map as the input FBCA.

**Example (copyOverExample.py)**
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
**Example Output:** 
``` shell
1 -> []
2 -> []
1 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54730>, <FBCAConsts.CACell object at 0x7fcf7cd45850>], [<FBCAConsts.CACell object at 0x7fcf7cd457f0>, <FBCAConsts.CACell object at 0x7fcf7ccd11f0>]]
2 -> []
1 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54730>, <FBCAConsts.CACell object at 0x7fcf7cd45850>], [<FBCAConsts.CACell object at 0x7fcf7cd457f0>, <FBCAConsts.CACell object at 0x7fcf7ccd11f0>]]
2 -> [[<FBCAConsts.CACell object at 0x7fcf7ce54520>, <FBCAConsts.CACell object at 0x7fcf7ccd1fa0>], [<FBCAConsts.CACell object at 0x7fcf7ccd16a0>, <FBCAConsts.CACell object at 0x7fcf7ccf22b0>]]
```

# makeFolder

A function that generates a folder provided it doesn’t already exist and the path is attainable. 

**Example call:**

makeFolder(directory)

**Argument:**

*directory*: Name of folder to be generated. **Do not forget to add /'s accordingly**

**Output:**

A folder of the name given in the current directory.


**Example code (makeFolderExample.py)**
```python
import FBCAConsts
import libFBCAGen
d = f"{libFBCAGen.os.getcwd()}/test/"
libFBCAGen.makeFolder(d)
```

Output: 
A file named test appears in the same folder testCode.py is.

# colourConvert

This is a simple switch function that returns a RGB tuple given an integer. The integer expected to be inputted in the state of a cell. For most applications, the first state is considered 'white space' in function of level-map generation, therefore changing this colour may yield nonsensical maps.

**Example call:**

colour = colourConvert(fBCA.levelMap[x][y].state)

**Argument:**

*x*: The state of a cell represented as an integer.

**Output:**

*x*: A RGB tuple represented as three integers. 

Due to this codes simplicity, no example code or output is shown.

# genIm

genIm visualizes FBCA as an image. This is done through converting each state into a colour for a png image using colourConvert. To generate the image, the PIL library is used. 

**Example call:**

genIm(exFBCA,quantifer = "/genIm")

**Argument:**

*fbca*: The desired FBCA to be visualized. Ideally this is initialized

*directory*: The desired location of the image. Defaults to the current working directory. **Do not forget to add /'s accordingly**

*quantifer*: The starting name of each file. The gen number is later tacked on. The default is 'test'

*gen*: The number current update being visualized. This is especially useful when generating multiple images. 


**Output:**

*im*: A RGB tuple represented as three integers. 




**Example code (genImExample.py)**
```python
import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
libFBCAGen.genIm(exFBCA,quantifer = "/genIm")
```
Output: 

The following image is saved into the folder 'genIm' in the current working directory

![L_0](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/genIm%200.png)

# updateMap

updateMap takes an existing FBCA and goes through one discrete time step. The updating function is mathematical defined as, [this hard to read thing](https://raw.githubusercontent.com/mkreitze/libFBCAGen/master/resources/update%20function.png). In more common terms, a cell takes the state of its highest scoring neighbour. The updating function occurs in three steps, first each score is determined. Then the level-map is copied. The original level-map is searched for highest scoring neighbours and states of the copied map are changed. This updated copy is then returned.

**Example call:**

fbca.levelMap = updateMap(fbca)

**Argument:**

*fbca*: The FBCA driving the update. It is assumed to be initialized. 

**Output:**

*CAMapCopy*: The updated list of states that represent the level-map

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

![L0](https://github.com/mkreitze/libFBCAGen/blob/master/resources/updateMapExample/updateMap%200.png)<br />
![L1](https://github.com/mkreitze/libFBCAGen/blob/master/resources/updateMapExample/updateMap%201.png)<br />
![L2](https://github.com/mkreitze/libFBCAGen/blob/master/resources/updateMapExample/updateMap%202.png)<br />
![L3](https://github.com/mkreitze/libFBCAGen/blob/master/resources/updateMapExample/updateMap%203.png)<br />
![L4](https://github.com/mkreitze/libFBCAGen/blob/master/resources/updateMapExample/updateMap%204.png)<br />

# genText

Saves an FBCA into a text document. This is done by first (optionally) saving the cells of the FBCA as a string of integers representing each cells state. Then (optionally) the following string;

sMs{fbca.scoreMatrix}g{fbca.g}n{fbca.n}w{fbca.torusWidth}l{fbca.torusLength}neighbours{fbca.neighbourhood}

then records the g (updates), n (number of states), torus width, torus length and each cells neighbourhood.

**Example call:**

genText(exFBCA,fileName = "genTextExample.txt")

**Argument:**

*fbca*: The FBCA to be recorded as text<br />
*directory*: File directory to save to. Defaults to the current working directory. **Do not forget to add /'s accordingly**<br />
*fileName*: Name of generated text file<br />
*newFile*: Boolean, if true, the old file will be written over. Defaults to true.<br />
*justMap*: Boolean, if true, only the states of the level-map will be recorded. Defaults to false.<br />
*noMap*: Boolean, if true, the states of the level-map will not be recorded. Defaults to false.<br />

**Output:**
A textfile named "fileName" in the specified directory (or current working directory if not specified)

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
**Output:** 
The following [text file](https://github.com/mkreitze/libFBCAGen/blob/master/resources/genTextExample/genTextExample.txt). 

# generateFBCA

**Example call:**

exFBCA.levelMap = generateFBCA(exFBCA,saveFinalImage=True, saveImages= True, saveFinalText = True, quantifer = "generateFBCAExample")

**Argument:**

*fbca*: The FBCA to be visualized and recorded<br />
*directory*: The directory all files will be saved to. Defaulted to current working directory.<br />
*quantifer*: The starting name of each file. Defaulted to 'test'<br />
*saveImages*: Boolean, if true, pngs of each update will be saved. Defaulted to False.<br />
*saveFinalImages*: Boolean, if true, saves a gif of all updates strung together. Defaulted to false.<br />
*saveText*: Boolean, if true, saves each update as an integer string to text file. Defaulted to false.<br />
*saveFinalText*: Boolean, if true, saves final update as an integer string and saves the FBCA parameters to text. Defaulted to false.<br />

**Output:**

*CAMap*: The final level-map from the FBCA run to its number of generations.

This function takes a _assumed to be initialized_ FBCA and fully generates it. It allows for it to be recorded through each update either as text or png image.   

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

[This folder](https://github.com/mkreitze/libFBCAGen/tree/master/resources/generateFBCAExample). 


# readFBCA

This function takes a (hopefully) textfile that has been produced by the genText function. It then reads it in but ignores any generated maps. This functionality may be added later. 

**Example call:**
listOfFBCAs = libFBCAGen.readFBCA(fileToReadFrom)

**Argument:**
*fileName*: The name of the (hopefully) textfile that stores the FBCA <br />

**Example code**
```python
import FBCAConsts
import libFBCAGen
# generate a text file
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
exFBCA.g = 6
libFBCAGen.genText(exFBCA,fileName = "readTextExample.txt")
# read from text
fileToReadFrom = "readTextExample.txt"
listOfFBCAs = libFBCAGen.readFBCA(fileToReadFrom)
print(listOfFBCAs[0].g)
print(listOfFBCAs[0].n)
print(listOfFBCAs[0].torusWidth)
print(listOfFBCAs[0].torusLength)
print(listOfFBCAs[0].scoreMatrix)
print(listOfFBCAs[0].neighbourhood)
# output
libFBCAGen.generateFBCA(exFBCA,quantifer = "/original",saveImages = True)
libFBCAGen.generateFBCA(listOfFBCAs[0],quantifer = "/new",saveImages = True)
```
**Output:**
``` shell
6
2
100
100
[0.0, 0.5, 0.2, 0.6]
[(0, 1), (0, -1), (-1, 0), (1, 0)]
```
And the following two FBCAs: 

![new](https://github.com/mkreitze/libFBCAGen/blob/master/resources/readTextExample/new.gif)<br />
![original](https://github.com/mkreitze/libFBCAGen/blob/master/resources/readTextExample/original.gif)<br />

**Code of all functions: (idk if i should keep)**

**initCA** 
```python
# Input: An FBCA 
# Output: A level-map pseudo-random collection of states
def initCA(fbca):
    #Fills in downward stripes as we iterate x then y
    for x in range(0,fbca.torusLength):
        holder=[] #downward column at the x value
        for y in range(0,fbca.torusWidth):
            holder.append(FBCAConsts.CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,FBCAConsts.numOfStates-1)
        fbca.levelMap.append(holder)
    return(fbca.levelMap)
```

**copyOver**
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

**makeFolder**
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
**colourConvert**
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
**genIm**
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
**updateMap**
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
**genText**
```python 
# Input: FBCA, directory, fileName, newFile, justMap, noMap
# Output: text file recording FBCA
def genText(fbca, directory = os.getcwd(), fileName = "test.txt", newFile = True, justMap = False, noMap = Falses):
    if newFile == True: 
        f = open(fileName, "w")
    else:
        f = open(fileName, "a")
    if noMap == False:
        for x in range(fbca.torusLength):
            for y in range(fbca.torusWidth):
                f.write(f"{fbca.levelMap[x][y].state}")
    f.write("\n")
    if justMap == False:
        f.write(f"sMs{fbca.scoreMatrix}g{fbca.g}n{fbca.n}w{fbca.torusWidth}l{fbca.torusLength}neighbours{fbca.neighbourhood}\n")
    return()
```
**generateFBCA**
```python
# Input: fbca, directory, quantifer
# Output: L_g for the system, if saved, L will be generated in as folder named by the quantifer.
def generateFBCA(fbca,directory = os.getcwd(),quantifer = "test", saveImages = False, saveFinalImage = False, saveText = False, saveFinalText = False):
    gif=[];CAMap=[];CAMap=copyOver(fbca) #PIL shenningans
    if (saveImages == True ) or (saveFinalImage == True ):
        directory=f"{directory}/{quantifer}/"
    makeFolder(directory)
    for n in range(fbca.g):
        if (saveImages == True):
            gif.append(genIm(fbca, directory, quantifer, gen = n))
        if (saveText == True):
            genText(fbca, directory, f"{directory}/{quantifer}.txt", justMap = True, newFile = False)
        fbca.levelMap=updateMap(fbca)
    if (saveFinalImage == True) or (saveImages == True):
        gif.append(genIm(fbca, directory, quantifer, fbca.g))
        gif[0].save(f"{directory}{quantifer}.gif",save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    if (saveText == True) or (saveFinalText == True):
        genText(fbca,directory, f"{directory}/{quantifer}.txt", justMap = False, newFile = False)
    return(CAMap)
```


