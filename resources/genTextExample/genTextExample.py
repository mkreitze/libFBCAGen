import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.scoreMatrix = [0,0.5,0.2,0.6]
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
exFBCA.g = 6
libFBCAGen.genText(exFBCA,fileName = "genTextExample.txt")