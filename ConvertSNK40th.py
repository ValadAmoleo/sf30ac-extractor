import extract
import tidy
import split
import sys

extractedFolder = "extracted/"
extract.extract(extractedFolder,"Bundle/")
split.begin_convert(extractedFolder,"roms",None,"snk40th")