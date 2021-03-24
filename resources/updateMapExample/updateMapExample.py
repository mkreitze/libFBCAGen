import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
totalNumOfGens = 5
for n in range(totalNumOfGens):
    libFBCAGen.genIm(exFBCA,gen = n, quantifer = "/updateMap")
    exFBCA.levelMap = libFBCAGen.updateMap(exFBCA)