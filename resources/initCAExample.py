import FBCAConsts
import libFBCAGen

exFBCA = FBCAConsts.Fbca()
exFBCA.torusLength = 2; exFBCA.torusWidth = 2
print (f"1 -> {exFBCA.levelMap}")
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
print (f"1 -> {exFBCA.levelMap}")