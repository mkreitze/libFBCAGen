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
libFBCAGen.generateFBCA(exFBCA,quantifer = "/original",saveImages = True)
libFBCAGen.generateFBCA(listOfFBCAs[0],quantifer = "/new",saveImages = True)