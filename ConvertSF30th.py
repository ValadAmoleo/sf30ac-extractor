import extract
import tidy
import split
import sys

extractedFolder = "extracted/"
extract.extract(extractedFolder,"Bundle/")
tidy.tidy(extractedFolder)
split.begin_convert(extractedFolder,"roms",None,None)