import FBCAConsts
import libFBCAGen
exFBCA = FBCAConsts.Fbca()
exFBCA.levelMap = libFBCAGen.initCA(exFBCA)
libFBCAGen.genIm(exFBCA,quantifer = "/genIm")