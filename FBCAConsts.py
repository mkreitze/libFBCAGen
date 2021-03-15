# Library made and documented in Jan 2020 by Matthew (Angelo) Kreitzer for his PhD research
# These are the 'global variables'
# Initalizations for FBCA generation; these are F,g,n,S,L_0

CALength=100  # (F)
CAWidth=100 # (F)
neighbours=[] # (F)
neighbours.append((0,1)) # (F)
neighbours.append((0,-1)) # (F)
neighbours.append((-1,0)) # (F)
neighbours.append((1,0)) # (F)
numOfGens = 40 # (g)
numOfStates = 2 # (n)
scoreMatrix = [1,2,3,4] # (S)

## DATA STRUCTURES

class Fbca:
    levelMap=[] # L_g
    scoreMatrix=[] # S
    behaviourNum=0 # iso-behavioural identification 
    g = numOfGens
    n = numOfStates
    neighbourhood = neighbours
    torusWidth = CAWidth
    torusLength = CALength


class CACell:
    state=0
    score=0
