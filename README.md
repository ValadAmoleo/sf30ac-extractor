# sf30ac-extractor
Extract assets from Street Fighter 30th Anniversary Collection, SNK 40th Anniversary Collection and Samurai Shodown Collection (ROMs, music, artwork, fonts, etc).

## Requirements
You need to have a python 3 available somewhere

## Usage
Download the project.

### Extract, Tidy & Convert
If you're looking just to extract the ROMs from a supported collection, you can now just extract the project files to the collection directory and run Convert.py.  This doesn't delete the extracted folder so that you can still browse the other data contained.

```
python Convert.py
```

### Extraction
Open a command line and execute the following command.

```
python extract.py "C:\.....\Street Fighter 30th Anniversary Collection\Bundle" "C:\...your extraction folder..."
```

The arguments are 1) the original bundle folder (in your steam directory) 2) the folder where you want stuff to be extracted to.

### Tidy-up
For some reason, the Second Impact music is in the Third Strike bundle, and the Third Strike music is in the Main bundle. If after extraction, you would like to move these files into the correct games' folder, you can execute the following command:

```
python tidy.py "C:\...your extraction folder..."
```

### Convert into MAME/FBN compatible ROMs
To convert all the currently compatible ROMs execute the following.

```
python split.py "...your extraction folder..." "...your rom folder..."
```
To convert a specific ROM or a specific collection execute the following and follow the instructions.
```
python split.py 
```

## Dependency
`bplist.py` was stolen by the project [bplist-python](https://github.com/farcaller/bplist-python) with a few alterations to make this work.
