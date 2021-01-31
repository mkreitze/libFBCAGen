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


            