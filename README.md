# sf30ac-extractor
Extract assets from Street Fighter 30th Anniversary Collection, SNK 40th Anniversary Collection and Samurai Shodown Collection (ROMs, music, artwork, fonts, etc).

Also converts ROM files from pre-extracted files from the SEGA AGES collection on Switch. Read the [Sega Ages section below](#sega-ages).

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

### SEGA Ages
As this tool can not extract games from Switch files or extract from CCF files you will need to do those manually.

Step 1:  Extract the SEGA AGES CCF files from the Switch.  I recommend using [NXDumpTool](https://github.com/DarkMatterCore/nxdumptool).  The CCF files are contained in /system/roms/ of the RomFS section.
Step 2:  Use CCFEX included on [this post](https://www.smspower.org/forums/post111289#111289) to extract the CCF files.
Step 3:  Place the files extracted into folders named the same as the CCF file you extracted them from.  E.g. put the files extracted from IchidantR_us into a folder called IchidantR_us.
Step 4:  Use this sf30ac-extractor tool with the following command:
```
python split.py "" "...your rom folder..." --type "segaages"
```

## Dependency
`bplist.py` was stolen by the project [bplist-python](https://github.com/farcaller/bplist-python) with a few alterations to make this work.

## Thanks
[petmac](https://github.com/petmac) and [WydD](https://github.com/WydD) for their work upstream.
[ghoost82](https://github.com/ghoost82) for their [CPS1 decoding work](https://github.com/WydD/sf30ac-extractor/issues/2#issuecomment-590633771).
[reubenajohnston](https://github.com/reubenajohnston) for their research.
[Vaiski](https://gitlab.com/vaiski) for their extraction work.
[scrap_a](http://blog.livedoor.jp/scrap_a) for their extraction work.
