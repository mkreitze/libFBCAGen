import FBCAConsts
import libFBCAGen

exFBCA = FBCAConsts.Fbca()
print (f"1 -> {exFBCA.levelMap}")
exFBCA.levelMap = libFBCAGen.initCA(exFBCA.levelMap,2,2)
print (exFBCA.levelMap)