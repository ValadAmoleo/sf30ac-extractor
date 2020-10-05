import os
import sys
import argparse
import zipfile

def usage():
    print("Usage: python split.py \"...ExtractionFolder...\" \"...RomFolder...\" --rom \"RomName\" --type \"ConversionType\"")
    print("RomName should be from: sf, sf2ub, sf2ceua, sf2t, ..., ..., ..., ..., ..., sfiiina, sfiii2n, sfiii3nr1")
    print("If you do not include --rom, all currently extractable roms will be extracted.")
    print("ConversionType can be sf30th, sfa1up or snk40th.  If you do not include this, sf30th will be used.")
    sys.exit(0)

conversion_type_streetfighter30th = "sf30th"

class Game(object):
    compatibility = []
    files = []
    def __init__(self, name, contained_within, extracted_folder_name, rom_name):
        self.name = name
        self.contained_within = contained_within
        self.extracted_folder_name = extracted_folder_name
        self.rom_name = rom_name
        
class GameFile(object):
    def __init__(self, filename, output_filenames):
        self.filename = filename
        self.output_filenames = output_filenames

class RenameGameFile(GameFile):
    def __init__(self, filename, output_filename):
        super().__init__(filename, output_filename)
        
class SplitGameFileEvenOdd(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size
       
class SplitGameFile(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size

def get_games():
    all_games = []
    SF30th_SF = Game("Street Fighter", conversion_type_streetfighter30th, "StreetFighter", "sf")
    SF30th_SF.compatibility.append("FB Neo")
    SF30th_SF.files.append(SplitGameFile("StreetFighter.bplanes.rom", ["sf-39.2k", "sf-38.1k", "sf-41.4k", "sf-40.3k"], 128 * 1024))
    SF30th_SF.files.append(SplitGameFile("StreetFighter.mplanes.rom", ["sf-25.1d", "sf-28.1e", "sf-30.1g", "sf-34.1h", "sf-26.2d", "sf-29.2e", "sf-31.2g", "sf-35.2h"], 128 * 1024))
    SF30th_SF.files.append(SplitGameFile("StreetFighter.sprites.rom", ["sf-15.1m", "sf-16.2m", "sf-11.1k", "sf-12.2k", "sf-07.1h", "sf-08.2h", "sf-03.1f", "sf-17.3m", "sf-18.4m", "sf-13.3k", "sf-14.4k", "sf-09.3h", "sf-10.4h","sf-05.3f"], 128 * 1024))
    SF30th_SF.files.append(RenameGameFile("StreetFighter.alpha.rom", "sf-27.4d"))
    SF30th_SF.files.append(SplitGameFile("StreetFighter.maps.rom", ["sf-37.4h", "sf-36.3h", "sf-32.3g", "sf-33.4g"], 64 * 1024))
    SF30th_SF.files.append(RenameGameFile("StreetFighter.z80", "sf-02.7k"))
    SF30th_SF.files.append(SplitGameFile("StreetFighter.u.samples.rom", ["sfu-00.1h", "sf-01.1k"], 128 * 1024))
    SF30th_SF.files.append(SplitGameFileEvenOdd("StreetFighter.u.68k", [("sfd-19.2a", "sfd-22.2c"),("sfd-20.3a", "sfd-23.3c"),("sfd-21.4a", "sfd-24.4c")], 64 * 1024))
    all_games.append(SF30th_SF)
    return all_games

def create_game_list(rom_name, conversion_type, all_games):
    returnList = []
    for game in all_games :
        if game.contained_within == conversion_type_streetfighter30th:
            returnList.append(game) 
        
    return returnList
    
def rename_file(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        contents = src.read()
        dst_path = os.path.join(dst_dir, file.output_filenames)
        with open(dst_path, "wb") as dst:
            dst.write(contents)

def split_file_evenodd(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print(src_path)
        for (dst_even_name, dst_odd_name) in file.output_filenames:
            print("\t" + dst_even_name + ", " + dst_odd_name)
            dst_even_path = os.path.join(dst_dir, dst_even_name)
            dst_odd_path = os.path.join(dst_dir, dst_odd_name)
            with open(dst_even_path, "wb") as dst_even:
                with open(dst_odd_path, "wb") as dst_odd:
                    for i in range(file.size):
                        dst_even.write(src.read(1))
                        dst_odd.write(src.read(1))
                        
def split_file_evenodd_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print(src_path)
        src.read(file.offset)
        for (dst_even_name, dst_odd_name) in file.output_filenames:
            print("\t" + dst_even_name + ", " + dst_odd_name)
            dst_even_path = os.path.join(dst_dir, dst_even_name)
            dst_odd_path = os.path.join(dst_dir, dst_odd_name)
            with open(dst_even_path, "wb") as dst_even:
                with open(dst_odd_path, "wb") as dst_odd:
                    for i in range(file.size):
                        dst_even.write(src.read(1))
                        dst_odd.write(src.read(1))
                        
def split_file(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print(src_path)
        for dst_name in file.output_filenames:
            print("\t" + dst_name)
            contents = src.read(file.size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)
                
def split_file_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print(src_path)
        src.read(file.offset)
        for dst_name in file.output_filenames:
            print("\t" + dst_name)
            contents = src.read(file.size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)

def zip_game(rom_dir, rom_name):
    zipname=rom_dir+'/'+rom_name+'.zip'
    zipdir=rom_dir+'/'+rom_name
    zipObj = zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED)
    for folderName, subfolders, filenames in os.walk(zipdir):
        for filename in filenames:
            # Add file to zip
            zipfileLocation=(zipdir+'/'+filename)
            zipObj.write(zipfileLocation, filename)
    print(rom_name + " has been zipped to " +zipname)

def rm_dir(dir):
    for folderName, subfolders, filenames in os.walk(dir):
        for filename in filenames:
            os.remove(folderName+'/'+filename)
        os.rmdir(folderName)

def process_game_list(root_dir, game_list, rom_dir):
    for game in game_list:
        for file in game.files:
            src_path = os.path.join(root_dir, game.extracted_folder_name, file.filename)
            dst_dir = os.path.join(rom_dir, game.rom_name)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            if isinstance(file, SplitGameFile):
                split_file(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileEvenOdd):
                split_file_evenodd(src_path, dst_dir, file)
            elif isinstance(file, RenameGameFile):
                rename_file(src_path, dst_dir, file)
        zip_game(rom_dir, game.rom_name)
        rm_dir(rom_dir+'/'+game.rom_name)

def begin_convert(root_dir, rom_dir, rom_name, conversion_type):
    if conversion_type == None :
        conversion_type = "sf30th"
	
    #create rom_dir if missing
    if not os.path.exists(rom_dir):
        os.mkdir(rom_dir)
        
    all_games = get_games()
    game_list = create_game_list(rom_name, conversion_type, all_games)
    process_game_list(root_dir, game_list, rom_dir)

def main(argc, argv):
    if argc < 3:
        usage()

    parser = argparse.ArgumentParser()
    parser.add_argument("extractFolderStr", help="Location for extraction", type=str)
    parser.add_argument("romFolderStr", help="Location for rom", type=str)
    parser.add_argument("--rom", "--r", help="rom name", type=str)
    parser.add_argument("--type", "--t", help="conversion type", type=str)

    args = parser.parse_args()

    root_dir = args.extractFolderStr
    rom_dir = args.romFolderStr
    rom_name = args.rom
    conversion_type = args.type
    
    begin_convert(root_dir, rom_dir, rom_name, conversion_type)

    exit(0)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
        