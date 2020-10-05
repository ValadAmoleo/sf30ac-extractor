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
conversion_type_streetfighterarcade1up = "sfa1up"
conversion_type_snk40th = "snk40th"

debug = None

class Game(object):
    def __init__(self, name, contained_within, extracted_folder_name, rom_name):
        self.name = name
        self.contained_within = contained_within
        self.extracted_folder_name = extracted_folder_name
        self.rom_name = rom_name
        self.compatibility = []
        self.files = []
        self.converted = False
        
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
       
class SplitGameFileInterleave4Cps1(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size
       
class SplitGameFileSwab(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size
       
class SplitGameFile(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size

def get_games():
    all_games = []
    sf30th_sf = Game("Street Fighter", conversion_type_streetfighter30th, "StreetFighter", "sf")
    sf30th_sf.compatibility.append("FB Neo")
    sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".bplanes.rom", ["sf-39.2k", "sf-38.1k", "sf-41.4k", "sf-40.3k"], 128 * 1024))
    sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".mplanes.rom", ["sf-25.1d", "sf-28.1e", "sf-30.1g", "sf-34.1h", "sf-26.2d", "sf-29.2e", "sf-31.2g", "sf-35.2h"], 128 * 1024))
    sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".sprites.rom", ["sf-15.1m", "sf-16.2m", "sf-11.1k", "sf-12.2k", "sf-07.1h", "sf-08.2h", "sf-03.1f", "sf-17.3m", "sf-18.4m", "sf-13.3k", "sf-14.4k", "sf-09.3h", "sf-10.4h","sf-05.3f"], 128 * 1024))
    sf30th_sf.files.append(RenameGameFile(sf30th_sf.extracted_folder_name +".alpha.rom", "sf-27.4d"))
    sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".maps.rom", ["sf-37.4h", "sf-36.3h", "sf-32.3g", "sf-33.4g"], 64 * 1024))
    sf30th_sf.files.append(RenameGameFile(sf30th_sf.extracted_folder_name +".z80", "sf-02.7k"))
    sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".u.samples.rom", ["sfu-00.1h", "sf-01.1k"], 128 * 1024))
    sf30th_sf.files.append(SplitGameFileEvenOdd(sf30th_sf.extracted_folder_name +".u.68k", [("sfd-19.2a", "sfd-22.2c"),("sfd-20.3a", "sfd-23.3c"),("sfd-21.4a", "sfd-24.4c")], 64 * 1024))
    all_games.append(sf30th_sf)
    
    sf30th_sf2ub = Game("Street Fighter II The World Warrior", conversion_type_streetfighter30th, "StreetFighterII", "sf2ub")
    sf30th_sf2ub.compatibility.extend(["MAME-2001", "MAME-2003", "MAME-2003 Plus", "MAME-2004", "MAME-2005", "MAME-2006", "MAME-2007"])
    sf30th_sf2ub.files.append(RenameGameFile(sf30th_sf2ub.extracted_folder_name +".z80", "sf2_09.bin"))
    sf30th_sf2ub.files.append(SplitGameFile(sf30th_sf2ub.extracted_folder_name +".oki", ["sf2_18.bin", "sf2_19.bin"], 128 * 1024))
    sf30th_sf2ub.files.append(SplitGameFileEvenOdd(sf30th_sf2ub.extracted_folder_name +".ub.68k", [("sf2u.30e", "sf2u.37e"),("sf2u.31e", "sf2u.38e"),("sf2u.28e", "sf2u.35e"),("sf2.29a", "sf2.36a")], 128 * 1024))
    sf30th_sf2ub.files.append(SplitGameFileInterleave4Cps1(sf30th_sf2ub.extracted_folder_name +".vrom",[("sf2_06.bin", "sf2_08.bin", "sf2_05.bin", "sf2_07.bin"),("sf2_15.bin", "sf2_17.bin", "sf2_14.bin", "sf2_16.bin"),("sf2_25.bin", "sf2_27.bin", "sf2_24.bin", "sf2_26.bin")], 512 * 1024))
    all_games.append(sf30th_sf2ub)
    
    sf30th_sf2ceua = Game("Street Fighter II' Champion Edition", conversion_type_streetfighter30th, "StreetFighterII_CE", "sf2ceua")
    sf30th_sf2ceua.compatibility.extend(["MAME-2001", "MAME-2003", "MAME-2003 Plus", "MAME-2004", "MAME-2005", "MAME-2006", "MAME-2007"])
    sf30th_sf2ceua.files.append(RenameGameFile(sf30th_sf2ceua.extracted_folder_name +".z80", "s92_09.bin"))
    sf30th_sf2ceua.files.append(SplitGameFile(sf30th_sf2ceua.extracted_folder_name +".oki", ["s92_18.bin", "s92_19.bin"], 128 * 1024))
    sf30th_sf2ceua.files.append(SplitGameFileSwab(sf30th_sf2ceua.extracted_folder_name +".ua.68k", [("s92u-23a"),("sf2ce.22"),("s92_21a.bin")], 512 * 1024))
    sf30th_sf2ceua.files.append(SplitGameFileInterleave4Cps1(sf30th_sf2ceua.extracted_folder_name +".vrom",[("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),("s92_10.bin","s92_11.bin", "s92_12.bin", "s92_13.bin")], 512 * 1024))    
    all_games.append(sf30th_sf2ceua)
    
    #Need to change the folder path on this one.  Can't remember the file structure for Arcade1Up though.
    sfa1up_sf2ceua = Game("Street Fighter II' Champion Edition", conversion_type_streetfighterarcade1up, "StreetFighterII_CE", "sf2ceua")
    sfa1up_sf2ceua.compatibility.extend(["MAME-2001", "MAME-2003", "MAME-2003 Plus", "MAME-2004", "MAME-2005", "MAME-2006", "MAME-2007"])
    sfa1up_sf2ceua.files.append(RenameGameFile(sfa1up_sf2ceua.extracted_folder_name +".z80", "s92_09.bin"))
    sfa1up_sf2ceua.files.append(SplitGameFile(sfa1up_sf2ceua.extracted_folder_name +".oki", ["s92_18.bin", "s92_19.bin"], 128 * 1024))
    sfa1up_sf2ceua.files.append(SplitGameFileSwab(sfa1up_sf2ceua.extracted_folder_name +".ua.68k", [("s92u-23a"),("sf2ce.22"),("s92_21a.bin")], 512 * 1024))
    sfa1up_sf2ceua.files.append(SplitGameFileInterleave4Cps1(sfa1up_sf2ceua.extracted_folder_name +".patch.vrom",[("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),("s92_10.bin","s92_11.bin", "s92_12.bin", "s92_13.bin")], 512 * 1024))    
    all_games.append(sfa1up_sf2ceua)
    
    sf30th_sf2t = Game("Street Fighter II': Hyper Fighting", conversion_type_streetfighter30th, "StreetFighterII_HF", "sf2t")
    sf30th_sf2t.compatibility.extend(["MAME-2001", "MAME-2003", "MAME-2003 Plus", "MAME-2004", "MAME-2005", "MAME-2006", "MAME-2007"])
    sf30th_sf2t.files.append(RenameGameFile(sf30th_sf2t.extracted_folder_name +".z80", "s92_09.bin"))
    sf30th_sf2t.files.append(SplitGameFile(sf30th_sf2t.extracted_folder_name +".oki", ["s92_18.bin", "s92_19.bin"], 128 * 1024))
    sf30th_sf2t.files.append(SplitGameFileSwab(sf30th_sf2t.extracted_folder_name +".u.68k", [("sf2_23a"),("sf2_22.bin"),("sf2_21.bin")], 512 * 1024))
    sf30th_sf2t.files.append(SplitGameFileInterleave4Cps1(sf30th_sf2t.extracted_folder_name +".u.vrom",[("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),("s2t_10.bin", "s2t_11.bin", "s2t_12.bin", "s2t_13.bin")], 512 * 1024))    
    all_games.append(sf30th_sf2t)
    
    sf30th_sfiiina = Game("Street Fighter III: New Generation", conversion_type_streetfighter30th, "StreetFighterIII", "sfiiina")
    sf30th_sfiiina.compatibility.extend(["FB Neo"])
    sf30th_sfiiina.files.append(SplitGameFile(sf30th_sfiiina.extracted_folder_name +".s1", ["sfiii-simm1.0", "sfiii-simm1.1", "sfiii-simm1.2", "sfiii-simm1.3"], 2097152))
    sf30th_sfiiina.files.append(SplitGameFile(sf30th_sfiiina.extracted_folder_name +".s3", ["sfiii-simm3.0", "sfiii-simm3.1", "sfiii-simm3.2", "sfiii-simm3.3", "sfiii-simm3.4", "sfiii-simm3.5", "sfiii-simm3.6", "sfiii-simm3.7"], 2097152))
    sf30th_sfiiina.files.append(SplitGameFile(sf30th_sfiiina.extracted_folder_name +".s4", ["sfiii-simm4.0", "sfiii-simm4.1", "sfiii-simm4.2", "sfiii-simm4.3", "sfiii-simm4.4", "sfiii-simm4.5", "sfiii-simm4.6", "sfiii-simm4.7"], 2097152))
    sf30th_sfiiina.files.append(SplitGameFile(sf30th_sfiiina.extracted_folder_name +".s5", ["sfiii-simm5.0", "sfiii-simm5.1"], 2097152))
    sf30th_sfiiina.files.append(RenameGameFile(sf30th_sfiiina.extracted_folder_name +".bios", "sfiii_euro.29f400.u2"))
    all_games.append(sf30th_sfiiina)
    
    sf30th_sfiii2n = Game("Street Fighter III: 2nd Impact", conversion_type_streetfighter30th, "StreetFighterIII_2ndImpact", "sfiii2n")
    sf30th_sfiii2n.compatibility.extend(["FB Neo"])
    sf30th_sfiii2n.files.append(SplitGameFile(sf30th_sfiii2n.extracted_folder_name +".s1", ["sfiii2-simm1.0", "sfiii2-simm1.1", "sfiii2-simm1.2", "sfiii2-simm1.3"], 2097152))
    sf30th_sfiii2n.files.append(SplitGameFile(sf30th_sfiii2n.extracted_folder_name +".s2", ["sfiii2-simm2.0", "sfiii2-simm2.1", "sfiii2-simm2.2", "sfiii2-simm2.3"], 2097152))
    sf30th_sfiii2n.files.append(SplitGameFile(sf30th_sfiii2n.extracted_folder_name +".s3", ["sfiii2-simm3.0", "sfiii2-simm3.1", "sfiii2-simm3.2", "sfiii2-simm3.3", "sfiii2-simm3.4", "sfiii2-simm3.5", "sfiii2-simm3.6", "sfiii2-simm3.7"], 2097152))
    sf30th_sfiii2n.files.append(SplitGameFile(sf30th_sfiii2n.extracted_folder_name +".s4", ["sfiii2-simm4.0", "sfiii2-simm4.1", "sfiii2-simm4.2", "sfiii2-simm4.3", "sfiii2-simm4.4", "sfiii2-simm4.5", "sfiii2-simm4.6", "sfiii2-simm4.7"], 2097152))
    sf30th_sfiii2n.files.append(SplitGameFile(sf30th_sfiii2n.extracted_folder_name +".s5", ["sfiii2-simm5.0", "sfiii2-simm5.1", "sfiii2-simm5.2", "sfiii2-simm5.3", "sfiii2-simm5.4", "sfiii2-simm5.5", "sfiii2-simm5.6", "sfiii2-simm5.7"], 2097152))
    sf30th_sfiii2n.files.append(RenameGameFile(sf30th_sfiii2n.extracted_folder_name +".bios", "sfiii2_usa.29f400.u2"))
    all_games.append(sf30th_sfiii2n)
    
    sf30th_sfiii3nr1 = Game("Street Fighter III: 3rd Strike", conversion_type_streetfighter30th, "StreetFighterIII_3rdStrike", "sfiii3nr1")
    sf30th_sfiii3nr1.compatibility.extend(["FB Neo"])
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".r1.s1", ["sfiii3-simm1.0", "sfiii3-simm1.1", "sfiii3-simm1.2", "sfiii3-simm1.3"], 2097152))
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".r1.s2", ["sfiii3-simm2.0", "sfiii3-simm2.1", "sfiii3-simm2.2", "sfiii3-simm2.3"], 2097152))
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".s3", ["sfiii3-simm3.0", "sfiii3-simm3.1", "sfiii3-simm3.2", "sfiii3-simm3.3", "sfiii3-simm3.4", "sfiii3-simm3.5", "sfiii3-simm3.6", "sfiii3-simm3.7"], 2097152))
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".s4", ["sfiii3-simm4.0", "sfiii3-simm4.1", "sfiii3-simm4.2", "sfiii3-simm4.3", "sfiii3-simm4.4", "sfiii3-simm4.5", "sfiii3-simm4.6", "sfiii3-simm4.7"], 2097152))
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".s5", ["sfiii3-simm5.0", "sfiii3-simm5.1", "sfiii3-simm5.2", "sfiii3-simm5.3", "sfiii3-simm5.4", "sfiii3-simm5.5", "sfiii3-simm5.6", "sfiii3-simm5.7"], 2097152))
    sf30th_sfiii3nr1.files.append(SplitGameFile(sf30th_sfiii3nr1.extracted_folder_name +".s6", ["sfiii3-simm6.0", "sfiii3-simm6.1", "sfiii3-simm6.2", "sfiii3-simm6.3", "sfiii3-simm6.4", "sfiii3-simm6.5", "sfiii3-simm6.6", "sfiii3-simm6.7"], 2097152))
    sf30th_sfiii3nr1.files.append(RenameGameFile(sf30th_sfiii3nr1.extracted_folder_name +".bios", "sfiii3_usa.29f400.u2"))
    all_games.append(sf30th_sfiii3nr1)
    
    snk40th_bbusters = Game("Beast Busters", conversion_type_snk40th, "DLC1", "bbusters")
    snk40th_bbusters.compatibility.extend(["FB Neo"])
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".audiocpu", "bb-1.e6"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".gfx1", "bb-10.l9"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".gfx4", "bb-back1.m4"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".gfx5", "bb-back2.m6"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".ymsnd", "bb-pcma.l5"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".ymsnd.deltat", "bb-pcma.l3"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".eeprom", "bbusters-eeprom.bin"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-6.e7"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-7.h7"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-8.a14"))
    snk40th_bbusters.files.append(RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-9.c14"))
    snk40th_bbusters.files.append(SplitGameFileEvenOdd(snk40th_bbusters.rom_name +".maincpu", [("bb-3.k10", "bb-5.k12"),("bb-2.k8", "bb-4.k11")], 128 * 1024))
    snk40th_bbusters.files.append(SplitGameFileSwab(snk40th_bbusters.rom_name +".gfx2", ["bb-f11.m16", "bb-f12.m13", "bb-f13.m12", "bb-f14.m11"], 512 * 1024))
    snk40th_bbusters.files.append(SplitGameFileSwab(snk40th_bbusters.rom_name +".gfx3", ["bb-f21.l10", "bb-f22.l12", "bb-f23.l13", "bb-f24.l15"], 512 * 1024))
    
    all_games.append(snk40th_bbusters)
    
    return all_games

def create_game_list(rom_name, conversion_type, all_games):
    returnList = []
    for game in all_games :
        if (rom_name == None or rom_name == "all" or rom_name == "" or rom_name == game.rom_name) and (conversion_type == None or conversion_type == "all" or conversion_type == "" or game.contained_within == conversion_type):
            returnList.append(game)
            
    if len(returnList) == 0 :
        if rom_name != "" and rom_name != None and conversion_type != "" and conversion_type != None:
            print("Extracting " +rom_name +" from " +conversion_type +" is unsupported at this time.")
        elif rom_name != "" and rom_name != None :
            print(rom_name +" is unsupported at this time.")
        elif conversion_type != "" and conversion_type != None :
            print(conversion_type +" is unsupported at this time.")
        
    return returnList
    
def rename_file(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        contents = src.read()
        dst_path = os.path.join(dst_dir, file.output_filenames)
        with open(dst_path, "wb") as dst:
            dst.write(contents)

def split_file_evenodd(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print_if_debug(src_path)
        for (dst_even_name, dst_odd_name) in file.output_filenames:
            print_if_debug("\t" + dst_even_name + ", " + dst_odd_name)
            dst_even_path = os.path.join(dst_dir, dst_even_name)
            dst_odd_path = os.path.join(dst_dir, dst_odd_name)
            with open(dst_even_path, "wb") as dst_even:
                with open(dst_odd_path, "wb") as dst_odd:
                    for i in range(file.size):
                        dst_even.write(src.read(1))
                        dst_odd.write(src.read(1))
                        
def split_file_evenodd_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print_if_debug(src_path)
        src.read(file.offset)
        for (dst_even_name, dst_odd_name) in file.output_filenames:
            print_if_debug("\t" + dst_even_name + ", " + dst_odd_name)
            dst_even_path = os.path.join(dst_dir, dst_even_name)
            dst_odd_path = os.path.join(dst_dir, dst_odd_name)
            with open(dst_even_path, "wb") as dst_even:
                with open(dst_odd_path, "wb") as dst_odd:
                    for i in range(file.size):
                        dst_even.write(src.read(1))
                        dst_odd.write(src.read(1))
                        
def split_file(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print_if_debug(src_path)
        for dst_name in file.output_filenames:
            print_if_debug("\t" + dst_name)
            contents = src.read(file.size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)
                
def split_file_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print_if_debug(src_path)
        src.read(file.offset)
        for dst_name in file.output_filenames:
            print_if_debug("\t" + dst_name)
            contents = src.read(file.size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)
                
def split_file_interleave_4_cps1(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        print_if_debug(src_path)
        print_if_debug("Decoding CPS1 Graphics")
        for (dst_name_1, dst_name_2, dst_name_3, dst_name_4) in file.output_filenames:
            print_if_debug("\t" + dst_name_1 + ", " + dst_name_2 + ", " + dst_name_3 + ", " + dst_name_4)
            dst_path_1 = os.path.join(dst_dir, dst_name_1)
            dst_path_2 = os.path.join(dst_dir, dst_name_2)
            dst_path_3 = os.path.join(dst_dir, dst_name_3)
            dst_path_4 = os.path.join(dst_dir, dst_name_4)
            with open(dst_path_1, "wb") as dst_1:
                with open(dst_path_2, "wb") as dst_2:
                    with open(dst_path_3, "wb") as dst_3:
                        with open(dst_path_4, "wb") as dst_4:
                            for i in range(file.size // 2):
                                data = decode_cps1_gfx(src.read(8))
                                dst_1.write(data[0:2])
                                dst_2.write(data[2:4])
                                dst_3.write(data[4:6])
                                dst_4.write(data[6:8])

def decode_cps1_gfx(data):
    buf = bytearray(data)
    for i in range(0, len(buf), 4):
        dwval = 0
        src = buf[i] + (buf[i + 1] << 8) + (buf[i + 2] << 16) + (buf[i + 3] << 24)

        for j in range(8):
            n = src >> (j * 4) & 0x0f
            if (n & 0x01):
                dwval |= 1 << (     7 - j)
            if (n & 0x02):
                dwval |= 1 << ( 8 + 7 - j)
            if (n & 0x04):
                dwval |= 1 << (16 + 7 - j)
            if (n & 0x08):
                dwval |= 1 << (24 + 7 - j)

        buf[i + 0] = (dwval)       & 0xff
        buf[i + 1] = (dwval >>  8) & 0xff
        buf[i + 2] = (dwval >> 16) & 0xff
        buf[i + 3] = (dwval >> 24) & 0xff
    return buf
    
def split_file_swab(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        for (dst_name) in file.output_filenames:
            print_if_debug("\t" + dst_name)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                for i in range(file.size // 2):
                    byte0=src.read(1)
                    byte1=src.read(1)
                    dst.write(byte1)
                    dst.write(byte0)
                    
def split_file_swab_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        src.read(file.offset)
        for (dst_name) in file.output_filenames:
            print_if_debug("\t" + dst_name)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                for i in range(file.size // 2):
                    byte0=src.read(1)
                    byte1=src.read(1)
                    dst.write(byte1)
                    dst.write(byte0)

def zip_game(rom_dir, game):
    zipname=rom_dir+'/'+game.rom_name+'.zip'
    zipdir=rom_dir+'/'+game.rom_name
    zipObj = zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED)
    for folderName, subfolders, filenames in os.walk(zipdir):
        for filename in filenames:
            # Add file to zip
            zipfileLocation=(zipdir+'/'+filename)
            zipObj.write(zipfileLocation, filename)
    print(game.name + " has been zipped to " +zipname)

def print_if_debug(msg) :
    if debug == True :
        print(msg)

def rm_dir(dir):
    for folderName, subfolders, filenames in os.walk(dir):
        for filename in filenames:
            os.remove(folderName+'/'+filename)
        os.rmdir(folderName)
        
def check_files_exist(root_dir, game):
    for file in game.files:
        src_path = os.path.join(root_dir, game.extracted_folder_name, file.filename)
        if os.path.exists(src_path) == False :
            return False

def process_game_list(root_dir, game_list, rom_dir):
    for game in game_list:
        if check_files_exist(root_dir, game) == False:
            print("Unable to extract " +game.name  +" (" +game.contained_within +"). Reason:  One or more files not found")
            continue
        print("Converting: " +game.name)
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
            elif isinstance(file, SplitGameFileInterleave4Cps1) :
                split_file_interleave_4_cps1(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileSwab) :
                split_file_swab(src_path, dst_dir, file)
        zip_game(rom_dir, game)
        print(game.name +" is compatible with " + ", ".join(game.compatibility))
        game.converted = True
        rm_dir(rom_dir+'/'+game.rom_name)

def begin_convert(root_dir, rom_dir, rom_name, conversion_type):
    #create rom_dir if missing
    if not os.path.exists(rom_dir):
        os.mkdir(rom_dir)
        
    all_games = get_games()
    game_list = create_game_list(rom_name, conversion_type, all_games)
    process_game_list(root_dir, game_list, rom_dir)
    end_convert(game_list)

def end_convert(game_list) :
    unsuccessfulList = []
    total = 0
    for game in game_list :
        if game.converted == False :
            unsuccessfulList.append(game.name +" (" +game.contained_within +")")
        total += 1
    if total == 0 :
        return
    unsuccessful = len(unsuccessfulList)
    successful = total-len(unsuccessfulList)
    print("Finished converting.")
    print(str(successful) +"/" +str(total) +" converted successfully.")
    if unsuccessful > 0 :
        print("Unsuccessful:")
        print("\n".join(unsuccessfulList))
        

def main(argc, argv):
    if argc < 3:
        usage()

    parser = argparse.ArgumentParser()
    parser.add_argument("extractFolderStr", help="Location for extraction", type=str)
    parser.add_argument("romFolderStr", help="Location for rom", type=str)
    parser.add_argument("--rom", "--r", help="rom name", type=str)
    parser.add_argument("--type", "--t", help="conversion type", type=str)
    parser.add_argument('--debug', "--d", "--v", help="enable debug", action='store_true', default='false')
    args = parser.parse_args()

    root_dir = args.extractFolderStr
    rom_dir = args.romFolderStr
    rom_name = args.rom
    conversion_type = args.type
    global debug
    debug = args.debug
    
    begin_convert(root_dir, rom_dir, rom_name, conversion_type)

    exit(0)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
        