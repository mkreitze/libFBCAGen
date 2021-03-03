# Library made and documented in Jan 2020 by Matthew (Angelo) Kreitzer for his PhD research
# This library mainly used for the following purposes:
# # Records all functions and code used to generate FBCA
# # Forcing myself to review code and publish code to GitHub

# imports from external libraries
import random
import FBCAConsts # constants


# L_0 generation #
### Input: A list full of CACells (representing an empty FBCA)
### Output: A list full of CACells with a pseudo-random collection of states
# Notes:
# L_0s are prefered to be constant for checking weak behavioural equivlance. 
# To do this, simply call initCA once and use the copyOver function (other methods lead to data loss) 
def initCA(CAMap,length = FBCAConsts.CALength, width = FBCAConsts.CAWidth):
    #Fills in downward stripes as we interate x then y
    for x in range(0,length):
        holder=[] #downward column at the x value
        for y in range(0,width):
            holder.append(FBCAConsts.CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,FBCAConsts.numOfStates-1)
        CAMap.append(holder)
    return(CAMap)


# Copying function #
### Input: A list full of CACells
### Output: Another list full cells with the same states as the input
# Notes:
# The standard copy method loses data for a list of classes.
def copyOver(CAMapInit,length = FBCAConsts.CALength, width = FBCAConsts.CAWidth):
    CAMap=[]
    for x in range(0,length):
        holder=[]
        for y in range(0,width):
            holder.append(FBCAConsts.CACell())
            holder[y].state=CAMapInit[x][y].state
        CAMap.append(holder)
    return(CAMap)

### DID ABOVE

# FBCA Updater #
### Input: An L_n (2d list of CACells), A score matrix (stored as a 1d list)
### Output: L_(n+1) (2d list of CACells)
# Notes:
# The update is done in 3 steps:
# # Assigns each cell its score
# # Generates a copy of the L_g
# # Updates the states of the copy by taking the highest score state of a cells neighbourhood
# # The copy is then returned
# # The default neighbourhood is Von Neumann and is defined by the neighbours function 
def updateMap(CAMap,scoreMatrix):

    for x in range(0,CALength):
        for y in range(0,CAWidth):
            #Need to get score from center square and its neighbours.
            row = CAMap[x][y].state*numOfStates #the center colour determines the row of the score matrix used 
            #new method to save a small amount of computation
            col0=CAMap[(x+neighbours[0][0])%CALength][(y+neighbours[0][1])%CAWidth].state 
            col1=CAMap[(x+neighbours[1][0])%CALength][(y+neighbours[1][1])%CAWidth].state 
            col2=CAMap[(x+neighbours[2][0])%CALength][(y+neighbours[2][1])%CAWidth].state 
            col3=CAMap[(x+neighbours[3][0])%CALength][(y+neighbours[3][1])%CAWidth].state
            CAMap[x][y].score=scoreMatrix[row+col0]+scoreMatrix[row+col1]+scoreMatrix[row+col2]+scoreMatrix[row+col3]
    #start by copying the map
    CAMapCopy=copyOver(CAMap)
    #for every cell, find the highest score among neighbours
    for x in range(0,CALength):
        for y in range(0,CAWidth):
            #NOTE: We give priority to the center square on ties. Priority continues up with the last defined neighbour to have the worst priority
            bigScore=0;bigScore=CAMap[x][y].score
            #compares neighbours scores, reassigning bigScore and state if someone is bigger
            for z in neighbours:
                if(bigScore<CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].score):
                    bigScore=CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].score
                    CAMapCopy[x][y].state=CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].state
    return(CAMapCopy)            

# Generation of FBCA #
##Input: Score matrix (as a one dimensional list), directory, L_0 and a quantifer
##Output: L_g for the system, if visualized L will be generated in a folder named by the quantifer.
# Notes:
# Since F,g,L_0,n are all constant, they are not needed for the generate FBCA function.
# The global variables useImages and finalImage dictate if visual records are kept for generated FBCAs
# The visual records come as a gif and L_g (I am having difficulty making it just a bunch of single images)
def generateFBCA(scoreMatrix,d,CAMapInit,quantifer):
    gif=[];CAMap=[];CAMap=copyOver(CAMapInit)
    if (useImages==1) or (finalImage==1):
        d=f"{d}/{quantifer}/"
    makeFolder(d)
    for n in range(numOfGens):
        if (useImages==1):
            gif.append(genIm(CAMap,numOfGens,d,quantifer))
        CAMap=updateMap(CAMap,scoreMatrix)
    if (finalImage==1):
        gif.append(genIm(CAMap,numOfGens,d,quantifer))
        gif[0].save(f"{d}{quantifer}.gif",save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    return(CAMap)

# Folder generation #
### Input: Name of a folder we want to make
### Output: True (1) or False (0) if folder is made 
def makeFolder(folderName):
    try: 
        os.makedirs(folderName)
        return(1)
    except:
        return(0)

# Image generation method #
### Input: L_n (2d list of CACell with states), n, folder name, 
### Output: An image file
# Notes:
# I have no idea what an image file is
def genIm(CAMap,n,directory=os.getcwd(),quantifer="giveName"):
    im= Image.new('RGB', (n, n))
    for x in range(n):
        for y in range(n):
            im.putpixel((x,y),colourConvert(CAMap[x][y]))
    im.save(f"{directory}{quantifer} {str(n)}.png")
    return(im)

# State to Colour converter #
### Input: state (as an int)
### Output: RGB touple
# Notes:
# When visualize through images, each state is given a colour. All colours are arbitrary with one exception:
# # Some evolutionary computation attempts to force certain behaviours by constraning the first state 
# # This was done to preserve 'open space' and as such the first state is always white.
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