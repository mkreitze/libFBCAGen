# Library made and documented in Jan 2020 by Matthew (Angelo) Kreitzer for his PhD research
# This library mainly used for the following purposes:
# # Records all functions and code used to generate FBCA
# # Forcing myself to review code and publish code to GitHub


# Initalizations for FBCA generation:
# F -> connectivity of each cell in the FBCA (its neighbourhood)
# g -> the number of updates done to an FBCA before completion 
# n -> number of states in the FBCA 
# 
numOfGens=40 #number of generations (g)
numOfStates=2 #number of states (n) [defined till 10]

# F
# F is defined as a torus and needs parameters to define this
CALength=100 #Length of torus (related to thickness of the torus) [for dB method use 5]
CAWidth=100 #Width of torus (related to radius of the torus) [for dB method use 4]
useMinMap=0 #honestly, something I have to fix
# F's connectivity is arbitrary. It is assumed each cell has the same connectivity.
# To represent the connectivity, a list of touples representing the x and y offset is needed
# The default is Von Neumann and is defined below
neighbours=[]
neighbours.append((0,1))#top (1 up)
neighbours.append((0,-1))#bot (1 down)
neighbours.append((-1,0))#left (1 left)
neighbours.append((1,0))#right (1 right)