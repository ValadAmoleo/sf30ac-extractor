import extract
import tidy
import split
import sys
import os

extractedFolder = "extracted/"

directory = os.path.basename(os.path.dirname(os.path.realpath(__file__))).lower()
if "street" in directory and "30th" in directory :
    print("You're trying to convert Street Fighter 30th Anniversary Edition")
    if os.path.exists(extractedFolder) == False :
        extract.extract(extractedFolder,"Bundle/")
        tidy.tidy(extractedFolder)
    split.begin_convert(extractedFolder,"roms",None,"sf30th", None, False)
elif "snk" in directory and "40th" in directory :
    print("You're trying to convert SNK 40th Anniversary Collection")
    if os.path.exists(extractedFolder) == False :
        extract.extract(extractedFolder,"Bundle/")
    split.begin_convert(extractedFolder,"roms",None,"snk40th", None, False)
elif "ss" in directory and "neogeo" in directory :
    print("You're trying to convert Samurai Shodown Collection")
    if os.path.exists(extractedFolder) == False :
        extract.extract(extractedFolder,"Bundle/")
    split.begin_convert(extractedFolder,"roms",None,"samsho", None, False)
else :
    print("Can't determine what you're trying to convert.  Please proceed manually.")