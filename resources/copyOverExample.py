import FBCAConsts
import libFBCAGen

exFBCA1 = FBCAConsts.Fbca()
exFBCA1.torusLength = 2; exFBCA1.torusWidth = 2
exFBCA2 = FBCAConsts.Fbca(); exFBCA2.levelMap = []
exFBCA2.torusLength = 2; exFBCA2.torusWidth = 2
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")
exFBCA1.levelMap = libFBCAGen.initCA(exFBCA1)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")
exFBCA2.levelMap = libFBCAGen.copyOver(exFBCA1)
print (f"1 -> {exFBCA1.levelMap}"); print (f"2 -> {exFBCA2.levelMap}")