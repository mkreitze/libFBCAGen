import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
f = open("threeFour.txt")
for line in f:
    badSM = line.split(" ")
    badSM[-1] = badSM[-1][:-1]
    for part in badSM:
        exFBCA.scoreMatrix.append(part)
exFBCA.n = 6
exFBCA.torusWidth = 200
exFBCA.torusLength = 400
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
exFBCA.g = 6
exFBCA.levelMap = libFBCAGen.generateFBCA(exFBCA,saveFinalImage=True, saveImages= True, saveFinalText = True, saveText = True, quantifer = "rand3")