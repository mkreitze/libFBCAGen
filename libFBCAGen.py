# Library made and documented in Jan 2020 by Matthew (Angelo) Kreitzer for his PhD research
# This library mainly used for the following purposes:
# # Records all functions and code used to generate FBCA
# # Forcing myself to review code and publish code to GitHub

# imports from external libraries
import random # for L_0 
import FBCAConsts # constants
import os # for folders
import time 
from PIL import Image #for visualization through image generation

# L_0 generation #
# Input: An FBCA 
# Output: A level-map pseudo-random collection of states
def initCA(fbca):
    #Fills in downward stripes as we interate x then y
    random.seed(time.clock_gettime_ns)
    for x in range(0,fbca.torusLength):
        holder=[] #downward column at the x value
        for y in range(0,fbca.torusWidth):
            holder.append(FBCAConsts.CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,fbca.n-1)
        fbca.levelMap.append(holder)
    return(fbca.levelMap)


# Copying function #
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


# Folder generation #
# Input: Name of a folder we want to make
# Output: True (1) or False (0) if folder is made 
def makeFolder(folderName):
    try: 
        os.makedirs(folderName)
        return(1)
    except:
        return(0)

# State to Colour converter #
# Input: state (as an int)
# Output: RGB touple
def colourConvert(x):
    return {
        0: (255,255,255), # you should never change white
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


# Image generation method #
# Input: A FBCA, folder name, quantifer
# Output: An image file
def genIm(fBCA, directory = os.getcwd(),quantifer="/", gen = 0):
    im = Image.new('RGB', (fBCA.torusLength, fBCA.torusWidth))
    for x in range(fBCA.torusLength):
        for y in range(fBCA.torusWidth):
            im.putpixel((x,y),colourConvert(fBCA.levelMap[x][y].state))
    im.save(f"{directory}{quantifer} {str(gen)}.png")
    return(im)


# Above is done #

# FBCA Updater #
# Input: FBCA to update
# Output: L_(n+1) (2d list of CACells)
def updateMap(fbca):

    for x in range(0,fbca.torusLength):
        for y in range(0,fbca.torusWidth):
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


# Above is done #

# Generation of text document representing FBCA # 
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

# Generation of FBCA #
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
            genText(fbca, directory, f"{quantifer}.txt", justMap = True, writeNewFile = False)
        fbca.levelMap=updateMap(fbca)
    if (saveFinalImage == True) or (saveImages == True):
        gif.append(genIm(fbca, directory, quantifer, fbca.g))
        gif[0].save(f"{directory}{quantifer}.gif",save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    if (saveText == True) or (saveFinalText == True):
        genText(fbca,directory, f"{quantifer}.txt", justMap = False, writeNewFile = False)
    return(CAMap)

