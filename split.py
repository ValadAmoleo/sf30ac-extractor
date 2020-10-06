import os
import sys
import argparse
import zipfile

def usage(game_list):
    print("Usage: python split.py \"...ExtractionFolder...\" \"...RomFolder...\" --rom \"RomName\" --type \"Collection\"")
    print("RomName should be from: " +game_list)
    print("If you do not include --rom, all currently extractable roms will be extracted.")
    print("Collection can be " +conversion_type_streetfighter30th +" , " +conversion_type_streetfighterarcade1up +", " +conversion_type_samuraishowdowncollection +" or "+conversion_type_snk40th +".")
    print("If you do not include --type, all currently extractable roms for all collections will be attempted.  The majority will fail depending on where you have this script.")
    sys.exit(0)

conversion_type_streetfighter30th = "sf30th"
conversion_type_streetfighterarcade1up = "sfa1up"
conversion_type_snk40th = "snk40th"
conversion_type_samuraishowdowncollection = "samsho"

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
        
class RenameGameFileOffset(GameFile):
    def __init__(self, filename, output_filename, offset):
        super().__init__(filename, output_filename)
        self.offset = offset
        
class SplitGameFileEvenOddOffset(GameFile):
    def __init__(self, filename, output_filenames, size, offset):
        super().__init__(filename, output_filenames)
        self.size = size
        self.offset = offset
        
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
        
class SplitGameFileSwabOffset(GameFile):
    def __init__(self, filename, output_filenames, size, offset):
        super().__init__(filename, output_filenames)
        self.size = size
        self.offset = offset
       
class SplitGameFile(GameFile):
    def __init__(self, filename, output_filenames, size):
        super().__init__(filename, output_filenames)
        self.size = size
       
class SplitGameFileOffset(GameFile):
    def __init__(self, filename, output_filenames, size, offset):
        super().__init__(filename, output_filenames)
        self.size = size
        self.offset = offset

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
    
    #Need to change the folder path on this one.  zassets\Capcom\StreetFighterII_CE.zip on the device.  Assume zassets is selected as the extracted folder.  In the future unzip automatically.
    sfa1up_sf2ceua = Game("Street Fighter II' Champion Edition", conversion_type_streetfighterarcade1up, "Capcom/StreetFighterII_CE.zip", "sf2ceua")
    sfa1up_sf2ceua.compatibility.extend(["MAME-2001", "MAME-2003", "MAME-2003 Plus", "MAME-2004", "MAME-2005", "MAME-2006", "MAME-2007"])
    sfa1up_sf2ceua.files.append(RenameGameFile("StreetFighterII_CE.z80", "s92_09.bin"))
    sfa1up_sf2ceua.files.append(SplitGameFile("StreetFighterII_CE.oki", ["s92_18.bin", "s92_19.bin"], 128 * 1024))
    sfa1up_sf2ceua.files.append(SplitGameFileSwab("StreetFighterII_CE.ua.68k", [("s92u-23a"),("sf2ce.22"),("s92_21a.bin")], 512 * 1024))
    sfa1up_sf2ceua.files.append(SplitGameFileInterleave4Cps1("StreetFighterII_CE.patch.vrom",[("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),("s92_10.bin","s92_11.bin", "s92_12.bin", "s92_13.bin")], 512 * 1024))    
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
    snk40th_bbusters.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_bbusters.files.append(SplitGameFileEvenOdd(snk40th_bbusters.rom_name +".maincpu", [("bb-3.k10", "bb-5.k12"),("bb-2.k8", "bb-4.k11")], 128 * 1024))
    snk40th_bbusters_audiocpu = RenameGameFile(snk40th_bbusters.rom_name +".audiocpu", "bb-1.e6")
    snk40th_bbusters.files.append(snk40th_bbusters_audiocpu)
    snk40th_bbusters_gfx1 = RenameGameFile(snk40th_bbusters.rom_name +".gfx1", "bb-10.l9")
    snk40th_bbusters.files.append(snk40th_bbusters_gfx1)
    snk40th_bbusters_gfx2 = SplitGameFileSwab(snk40th_bbusters.rom_name +".gfx2", ["bb-f11.m16", "bb-f12.m13", "bb-f13.m12", "bb-f14.m11"], 512 * 1024)
    snk40th_bbusters.files.append(snk40th_bbusters_gfx2)
    snk40th_bbusters_gfx3 = SplitGameFileSwab(snk40th_bbusters.rom_name +".gfx3", ["bb-f21.l10", "bb-f22.l12", "bb-f23.l13", "bb-f24.l15"], 512 * 1024)
    snk40th_bbusters.files.append(snk40th_bbusters_gfx3)
    snk40th_bbusters_gfx4 = RenameGameFile(snk40th_bbusters.rom_name +".gfx4", "bb-back1.m4")
    snk40th_bbusters.files.append(snk40th_bbusters_gfx4)
    snk40th_bbusters_gfx5 = RenameGameFile(snk40th_bbusters.rom_name +".gfx5", "bb-back2.m6")
    snk40th_bbusters.files.append(snk40th_bbusters_gfx5)
    snk40th_bbusters_scaletable1 = RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-6.e7")
    snk40th_bbusters_scaletable2 = RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-7.h7")
    snk40th_bbusters_scaletable3 = RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-8.a14")
    snk40th_bbusters_scaletable4 = RenameGameFile(snk40th_bbusters.rom_name +".scale_table", "bb-9.c14")
    snk40th_bbusters.files.append(snk40th_bbusters_scaletable1)
    snk40th_bbusters.files.append(snk40th_bbusters_scaletable2)
    snk40th_bbusters.files.append(snk40th_bbusters_scaletable3)
    snk40th_bbusters.files.append(snk40th_bbusters_scaletable4)
    snk40th_bbusters_ymsnd = RenameGameFile(snk40th_bbusters.rom_name +".ymsnd", "bb-pcma.l5")
    snk40th_bbusters.files.append(snk40th_bbusters_ymsnd)
    snk40th_bbusters_ymsnddeltat = RenameGameFile(snk40th_bbusters.rom_name +".ymsnd.deltat", "bb-pcma.l3")
    snk40th_bbusters.files.append(snk40th_bbusters_ymsnddeltat)
    snk40th_bbusters_eeprom = RenameGameFile(snk40th_bbusters.rom_name +".eeprom", "bbusters-eeprom.bin")
    snk40th_bbusters.files.append(snk40th_bbusters_eeprom)
    all_games.append(snk40th_bbusters)
    
    snk40th_bbustersu = Game("Beast Busters (US, Version 3)", conversion_type_snk40th, "DLC1", "bbustersu")
    snk40th_bbustersu.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_bbustersu.files.append(SplitGameFileEvenOdd(snk40th_bbustersu.rom_name +".maincpu", [("bb-ver3-u3.k10", "bb-ver3-u5.k12"),("bb-2.k8", "bb-4.k11")], 128 * 1024))
    snk40th_bbustersu.files.append(snk40th_bbusters_audiocpu)
    snk40th_bbustersu.files.append(snk40th_bbusters_gfx1)
    snk40th_bbustersu.files.append(snk40th_bbusters_gfx2)
    snk40th_bbustersu.files.append(snk40th_bbusters_gfx3)
    snk40th_bbustersu.files.append(snk40th_bbusters_gfx4)
    snk40th_bbustersu.files.append(snk40th_bbusters_gfx5)
    snk40th_bbustersu.files.append(snk40th_bbusters_scaletable1)
    snk40th_bbustersu.files.append(snk40th_bbusters_scaletable2)
    snk40th_bbustersu.files.append(snk40th_bbusters_scaletable3)
    snk40th_bbustersu.files.append(snk40th_bbusters_scaletable4)
    snk40th_bbustersu.files.append(snk40th_bbusters_ymsnd)
    snk40th_bbustersu.files.append(snk40th_bbusters_eeprom)    
    all_games.append(snk40th_bbustersu)
    
    snk40th_bbustersj = Game("Beast Busters (Japan, Version 2)", conversion_type_snk40th, "DLC1", "bbustersj")
    snk40th_bbustersj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_bbustersj.files.append(SplitGameFileEvenOdd(snk40th_bbustersj.rom_name +".maincpu", [("bb-ver2-j3.k10", "bb-ver2-j3.k12"),("bb-2.k8", "bb-4.k11")], 128 * 1024))
    snk40th_bbustersj.files.append(snk40th_bbusters_audiocpu)
    snk40th_bbustersj.files.append(snk40th_bbusters_gfx1)
    snk40th_bbustersj.files.append(snk40th_bbusters_gfx2)
    snk40th_bbustersj.files.append(snk40th_bbusters_gfx3)
    snk40th_bbustersj.files.append(snk40th_bbusters_gfx4)
    snk40th_bbustersj.files.append(snk40th_bbusters_gfx5)
    snk40th_bbustersj.files.append(snk40th_bbusters_scaletable1)
    snk40th_bbustersj.files.append(snk40th_bbusters_scaletable2)
    snk40th_bbustersj.files.append(snk40th_bbusters_scaletable3)
    snk40th_bbustersj.files.append(snk40th_bbusters_scaletable4)
    snk40th_bbustersj.files.append(snk40th_bbusters_ymsnd)
    snk40th_bbustersj.files.append(snk40th_bbusters_ymsnddeltat)
    snk40th_bbustersj.files.append(snk40th_bbusters_eeprom)    
    all_games.append(snk40th_bbustersj)    
    
    snk40th_chopperb = Game("Chopper I", conversion_type_snk40th, "Patch1", "chopperb")
    snk40th_chopperb.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_chopperb.files.append(RenameGameFile("chopper" +".maincpu", "kk_01.8g"))
    snk40th_chopperb.files.append(RenameGameFile("chopper" +".sub", "kk_04.6g"))
    snk40th_chopperb_audiocpu = RenameGameFile("chopper" +".audiocpu", "kk_03.3d")
    snk40th_chopperb.files.append(snk40th_chopperb_audiocpu)
    snk40th_chopperb.files.append(SplitGameFile("chopper" +".proms", ["k1.9w", "k3.9u", "k2.9v"], 1024))
    snk40th_chopperb_txtiles = RenameGameFile("chopper" +".tx_tiles", "kk_05.8p")
    snk40th_chopperb.files.append(snk40th_chopperb_txtiles)
    snk40th_chopperb_bgtiles = SplitGameFile("chopper" +".bg_tiles", ["kk_10.8y", "kk_11.8z", "kk_12.8ab", "kk_13.8ac"], 65536)
    snk40th_chopperb.files.append(snk40th_chopperb_bgtiles)
    snk40th_chopperb_sp16tiles = SplitGameFile("chopper" +".sp16_tiles", ["kk_09.3k", "kk_08.3l", "kk_07.3n", "kk_06.3p"], 32768)
    snk40th_chopperb.files.append(snk40th_chopperb_sp16tiles)
    snk40th_chopperb_sp32tiles = SplitGameFile("chopper" +".sp32_tiles", ["kk_18.3ab", "kk_19.2ad", "kk_20.3y", "kk_21.3aa","kk_14.3v", "kk_15.3x", "kk_16.3s", "kk_17.3t"], 65536)
    snk40th_chopperb.files.append(snk40th_chopperb_sp32tiles)
    snk40th_chopperb_ym2 = RenameGameFile("chopper" +".ym2", "kk_2.3j")
    snk40th_chopperb.files.append(snk40th_chopperb_ym2)
    snk40th_chopperb_plds = RenameGameFile("chopper" +".plds", "pal16r6b.2c")
    snk40th_chopperb.files.append(snk40th_chopperb_plds)
    all_games.append(snk40th_chopperb)
    
    snk40th_legofair = Game("Koukuu Kihei Monogatari - The Legend of Air Cavalry (Japan) - Chopper I", conversion_type_snk40th, "Patch1", "legofair")
    snk40th_legofair.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_legofair.files.append(RenameGameFile(snk40th_legofair.rom_name +".maincpu", "up03_m4.rom"))
    snk40th_legofair.files.append(RenameGameFile(snk40th_legofair.rom_name +".sub", "up03_m8.rom"))
    snk40th_legofair.files.append(snk40th_chopperb_audiocpu)
    snk40th_legofair.files.append(SplitGameFile("chopper" +".proms", ["up03_k1.rom", "up03_l1.rom", "up03_k2.rom"], 1024))
    snk40th_legofair.files.append(snk40th_chopperb_txtiles)
    snk40th_legofair.files.append(snk40th_chopperb_bgtiles)
    snk40th_legofair.files.append(snk40th_chopperb_sp16tiles)
    snk40th_legofair.files.append(snk40th_chopperb_sp32tiles)
    snk40th_legofair.files.append(snk40th_chopperb_ym2)
    snk40th_legofair.files.append(snk40th_chopperb_plds)
    all_games.append(snk40th_legofair)
    
    snk40th_ikari3 = Game("Ikari III: The Rescue", conversion_type_snk40th, "Main", "ikari3")
    snk40th_ikari3.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_ikari3.files.append(SplitGameFileEvenOdd(snk40th_ikari3.rom_name +".maincpu", [("ik3-2-ver1.c10", "ik3-3-ver1.c9")], 128 * 1024))
    snk40th_ikari3_user1 = SplitGameFileEvenOdd(snk40th_ikari3.rom_name +".user1", [("ik3-1.c8", "ik3-4.c12")], 64 * 1024)
    snk40th_ikari3.files.append(snk40th_ikari3_user1)
    snk40th_ikari3_soundcpu = RenameGameFile(snk40th_ikari3.rom_name +".soundcpu", "ik3-5.16d")
    snk40th_ikari3.files.append(snk40th_ikari3_soundcpu)
    snk40th_ikari3_gfx1 = SplitGameFile(snk40th_ikari3.rom_name +".gfx1", ["ik3-7.16l", "ik3-8.16m"], 32768)
    snk40th_ikari3.files.append(snk40th_ikari3_gfx1)
    snk40th_ikari3_gfx2 = SplitGameFileEvenOdd(snk40th_ikari3.rom_name +".gfx2", [("ik3-23.bin", "ik3-13.bin"), ("ik3-22.bin","ik3-12.bin"), ("ik3-21.bin","ik3-11.bin"), ("ik3-20.bin","ik3-10.bin"), ("ik3-19.bin","ik3-9.bin")], 131072)
    snk40th_ikari3.files.append(snk40th_ikari3_gfx2)
    snk40th_ikari3_gfx2_2 = SplitGameFileEvenOddOffset(snk40th_ikari3.rom_name +".gfx2", [("ik3-14.bin", "ik3-24.bin"), ("ik3-15.bin","ik3-25.bin"), ("ik3-16.bin","ik3-26.bin"), ("ik3-17.bin","ik3-27.bin"), ("ik3-18.bin","ik3-28.bin")], 131072, 131072*16)
    snk40th_ikari3.files.append(snk40th_ikari3_gfx2_2)
    snk40th_ikari3_upd = RenameGameFile(snk40th_ikari3.rom_name +".upd", "ik3-6.18e")
    snk40th_ikari3.files.append(snk40th_ikari3_upd)
    all_games.append(snk40th_ikari3)
    
    snk40th_ikari3u = Game("Ikari III: The Rescue (US)", conversion_type_snk40th, "Main", "ikari3u")
    snk40th_ikari3u.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_ikari3u.files.append(SplitGameFileEvenOdd(snk40th_ikari3u.rom_name +".maincpu", [("ik3-2.c10", "ik3-3.c9")], 128 * 1024))
    snk40th_ikari3u.files.append(snk40th_ikari3_user1)
    snk40th_ikari3u.files.append(snk40th_ikari3_soundcpu)
    snk40th_ikari3u.files.append(snk40th_ikari3_gfx1)
    snk40th_ikari3u.files.append(snk40th_ikari3_gfx2)
    snk40th_ikari3u.files.append(snk40th_ikari3_gfx2_2)
    snk40th_ikari3u.files.append(snk40th_ikari3_upd)
    all_games.append(snk40th_ikari3u)
    
    snk40th_ikari3j = Game("Ikari III: The Rescue (Japan)", conversion_type_snk40th, "Main", "ikari3j")
    snk40th_ikari3j.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_ikari3j.files.append(SplitGameFileEvenOdd(snk40th_ikari3j.rom_name +".maincpu", [("ik3-2-j.c10", "ik3-3-j.c9")], 128 * 1024))
    snk40th_ikari3j.files.append(snk40th_ikari3_user1)
    snk40th_ikari3j.files.append(snk40th_ikari3_soundcpu)
    snk40th_ikari3j.files.append(snk40th_ikari3_gfx1)
    snk40th_ikari3j.files.append(snk40th_ikari3_gfx2)
    snk40th_ikari3j.files.append(snk40th_ikari3_gfx2_2)
    snk40th_ikari3j.files.append(snk40th_ikari3_upd)
    all_games.append(snk40th_ikari3j)
    
    snk40th_ikari3k = Game("Ikari III: The Rescue (Korea)", conversion_type_snk40th, "Main", "ikari3k")
    snk40th_ikari3k.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_ikari3k.files.append(SplitGameFileEvenOdd(snk40th_ikari3k.rom_name +".maincpu", [("ik3-2k.c10", "ik3-3k.c9")], 128 * 1024))
    snk40th_ikari3k.files.append(snk40th_ikari3_user1)
    snk40th_ikari3k.files.append(snk40th_ikari3_soundcpu)
    snk40th_ikari3k.files.append(SplitGameFile(snk40th_ikari3k.rom_name +".gfx1", ["ik3-7k.16l", "ik3-8k.16m"], 32768))
    snk40th_ikari3k.files.append(SplitGameFileEvenOdd(snk40th_ikari3.rom_name +".gfx2", [("ikari-880d_t53.d2", "ikari-880c_t54.c2")], 131072 * 4))
    snk40th_ikari3k.files.append(SplitGameFileEvenOddOffset(snk40th_ikari3.rom_name +".gfx2", [("ik12.d1", "ik11.c1")], 131072, 131072 * 8))
    snk40th_ikari3k.files.append(SplitGameFileEvenOddOffset(snk40th_ikari3.rom_name +".gfx2", [("ikari-880d_t52.b2", "ikari-880c_t51.a2")], 131072 * 4, 131072 * 16))
    snk40th_ikari3k.files.append(SplitGameFileEvenOddOffset(snk40th_ikari3.rom_name +".gfx2", [("ik10.b1", "ik9.a1")], 131072, 131072 * 24))
    snk40th_ikari3k.files.append(snk40th_ikari3_upd)
    all_games.append(snk40th_ikari3k)
    
    snk40th_joyfulr = Game("Joyful Road (Japan) - Munch Mobile", conversion_type_snk40th, "Patch1", "joyfulr")
    snk40th_joyfulr.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_joyfulr.files.append(SplitGameFile(snk40th_joyfulr.rom_name +".maincpu", ["m1.10e", "m2.10d"], 8192))    
    snk40th_joyfulr.files.append(SplitGameFile(snk40th_joyfulr.rom_name +".maincpu", ["m1.10e", "m2.10d"], 8192))  
    snk40th_joyfulr_audiocpu = RenameGameFile(snk40th_joyfulr.rom_name +".audiocpu", "mu.2j");
    snk40th_joyfulr.files.append(snk40th_joyfulr_audiocpu) 
    snk40th_joyfulr_gfx1 = SplitGameFile(snk40th_joyfulr.rom_name +".gfx1", ["s1.10a", "s2.10b"], 4096)
    snk40th_joyfulr.files.append(snk40th_joyfulr_gfx1)  
    snk40th_joyfulr_gfx2 = SplitGameFile(snk40th_joyfulr.rom_name +".gfx2", ["b1.2c", "b1.2b"], 4096) 
    snk40th_joyfulr.files.append(snk40th_joyfulr_gfx2)
    snk40th_joyfulr.files.append(SplitGameFile(snk40th_joyfulr.rom_name +".gfx3", ["f1j.1g", "f2j.3g", "f3j.5g"], 8192)) 
    snk40th_joyfulr_gfx4 = RenameGameFile(snk40th_joyfulr.rom_name +".gfx4", "h");
    snk40th_joyfulr.files.append(snk40th_joyfulr_gfx4)
    snk40th_joyfulr_proms = RenameGameFile(snk40th_joyfulr.rom_name +".proms", "a2001.clr");
    snk40th_joyfulr.files.append(snk40th_joyfulr_proms)
    all_games.append(snk40th_joyfulr)
    
    snk40th_mnchmobl = Game("Munch Mobile", conversion_type_snk40th, "Patch1", "mnchmobl")
    snk40th_mnchmobl.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_mnchmobl.files.append(SplitGameFile(snk40th_mnchmobl.rom_name +".maincpu", ["m1.10e", "m2.10d"], 8192))    
    snk40th_mnchmobl.files.append(SplitGameFile(snk40th_mnchmobl.rom_name +".maincpu", ["m1.10e", "m2.10d"], 8192)) 
    snk40th_mnchmobl.files.append(snk40th_joyfulr_audiocpu)  
    snk40th_mnchmobl.files.append(snk40th_joyfulr_gfx1)
    snk40th_mnchmobl.files.append(snk40th_joyfulr_gfx2)    
    snk40th_mnchmobl.files.append(SplitGameFile(snk40th_mnchmobl.rom_name +".gfx3", ["f1.1g", "f2.3g", "f3.5g"], 8192))   
    snk40th_mnchmobl.files.append(snk40th_joyfulr_gfx4) 
    snk40th_mnchmobl.files.append(snk40th_joyfulr_proms)
    all_games.append(snk40th_mnchmobl)
    
    snk40th_ozmawars = Game("Ozma Wars", conversion_type_snk40th, "Patch1", "ozmawars")
    snk40th_ozmawars.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_ozmawars.files.append(SplitGameFile(snk40th_ozmawars.rom_name +".maincpu", ["mw01", "mw02", "mw03", "mw04"], 2048))
    snk40th_ozmawars.files.append(SplitGameFileOffset(snk40th_ozmawars.rom_name +".maincpu", ["mw05", "mw06"], 2048, 16384))
    snk40th_ozmawars.files.append(SplitGameFile("moonbase.proms", ["01.1", "02.2"], 1024))  
    all_games.append(snk40th_ozmawars)
    
    snk40th_fantasyu = Game("Fantasy", conversion_type_snk40th, "Patch1", "fantasyu")
    snk40th_fantasyu.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_fantasyu.files.append(SplitGameFile(snk40th_fantasyu.rom_name +".maincpu", ["ic12", "ic07", "ic08", "ic09", "ic10", "ic14", "ic15", "ic16", "ic17"], 4096))
    snk40th_fantasyu_gfx1 = SplitGameFile(snk40th_fantasyu.rom_name +".gfx1", ["fs10ic50.bin", "fs11ic51.bin"], 4096)    
    snk40th_fantasyu.files.append(snk40th_fantasyu_gfx1)
    snk40th_fantasyu.files.append(SplitGameFile(snk40th_fantasyu.rom_name +".proms", ["fantasy.ic7", "fantasy.ic6"], 32))
    snk40th_fantasyu_snk6502 = SplitGameFile(snk40th_fantasyu.rom_name +".snk6502", ["fs_b_51.bin", "fs_a_52.bin", "fs_c_53.bin"], 2048)
    snk40th_fantasyu.files.append(snk40th_fantasyu_snk6502)
    snk40th_fantasyu_speech = SplitGameFile(snk40th_fantasyu.rom_name +".speech", ["fs_d_7.bin", "fs_e_8.bin", "fs_f_11.bin"], 2048)
    snk40th_fantasyu.files.append(snk40th_fantasyu_speech)
    all_games.append(snk40th_fantasyu)
    
    snk40th_fantasyj = Game("Fantasy (Japan)", conversion_type_snk40th, "Patch1", "fantasyj")
    snk40th_fantasyj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_fantasyj.files.append(SplitGameFile(snk40th_fantasyj.rom_name +".maincpu", ["fs5jic12.bin", "fs1jic7.bin", "fs2jic8.bin", "fs3jic9.bin", "fs4jic10.bin", "fs6jic14.bin", "fs7jic15.bin", "fs8jic16.bin", "fs9jic17.bin"], 4096))
    snk40th_fantasyj.files.append(snk40th_fantasyu_gfx1)
    snk40th_fantasyj.files.append(SplitGameFile(snk40th_fantasyj.rom_name +".proms", ["prom-8.bpr", "prom-7.bpr"], 32))
    snk40th_fantasyj.files.append(snk40th_fantasyu_snk6502)
    snk40th_fantasyj.files.append(snk40th_fantasyu_speech)
    all_games.append(snk40th_fantasyj)
    
    snk40th_pow = Game("P.O.W.: Prisoners of War", conversion_type_snk40th, "Main", "pow")
    snk40th_pow.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_pow.files.append(SplitGameFileEvenOdd(snk40th_pow.rom_name +".maincpu", [("dg1ver1.j14", "dg2ver1.l14")], 128 * 1024))
    snk40th_pow_soundcpu = RenameGameFile(snk40th_pow.rom_name +".soundcpu", "dg8.e25");
    snk40th_pow.files.append(snk40th_pow_soundcpu)
    snk40th_pow_gfx1 = SplitGameFile(snk40th_pow.rom_name +".gfx1", ["dg9.l25", "dg10.m25"], 32 * 1024)
    snk40th_pow.files.append(snk40th_pow_gfx1)
    snk40th_pow_gfx2 = SplitGameFileEvenOdd(snk40th_pow.rom_name +".gfx2", [("snk880.11a", "snk880.15a"), ("snk880.12a","snk880.16a"), ("snk880.13a","snk880.17a"), ("snk880.14a","snk880.18a"), ("snk880.19a","snk880.23a"), ("snk880.20a","snk880.24a"), ("snk880.21a","snk880.25a"), ("snk880.22a","snk880.26a")], 128 * 1024)
    snk40th_pow.files.append(snk40th_pow_gfx2)
    snk40th_pow_upd = RenameGameFile(snk40th_pow.rom_name +".upd", "dg7.d20");
    snk40th_pow.files.append(snk40th_pow_upd)
    snk40th_pow_plds = RenameGameFile(snk40th_pow.rom_name +".plds", "pal20l10.a6");
    snk40th_pow.files.append(snk40th_pow_plds)
    all_games.append(snk40th_pow)
    
    snk40th_powj = Game("Datsugoku -Prisoners of War- (Japan)", conversion_type_snk40th, "Main", "powj")
    snk40th_powj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_powj.files.append(SplitGameFileEvenOdd(snk40th_powj.rom_name +".maincpu", [("1-2", "2-2")], 128 * 1024))
    snk40th_powj.files.append(snk40th_pow_soundcpu)
    snk40th_powj.files.append(snk40th_pow_gfx1)
    snk40th_powj.files.append(snk40th_pow_gfx2)
    snk40th_powj.files.append(snk40th_pow_upd)
    snk40th_powj.files.append(snk40th_pow_plds)
    all_games.append(snk40th_powj)
    
    snk40th_prehisle = Game("Prehistoric Isle in 1930", conversion_type_snk40th, "Main", "prehisle")
    snk40th_prehisle.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_prehisle.files.append(SplitGameFileEvenOdd("PrehistoricIsleIn1930.w.68k", [("gt-e2.2h", "gt-e3.3h")], 128 * 1024))
    snk40th_prehisle_z80 = RenameGameFile("PrehistoricIsleIn1930.z80", "gt1.1")
    snk40th_prehisle.files.append(snk40th_prehisle_z80)
    snk40th_prehisle_walpharom = RenameGameFile("PrehistoricIsleIn1930.w.alpha.rom", "gt15.b15")
    snk40th_prehisle.files.append(snk40th_prehisle_walpharom)
    snk40th_prehisle_bgrom = RenameGameFile("PrehistoricIsleIn1930.bg.rom", "gt8914.b14")
    snk40th_prehisle.files.append(snk40th_prehisle_bgrom)
    snk40th_prehisle_fgrom = RenameGameFile("PrehistoricIsleIn1930.fg.rom", "pi8916.b14")
    snk40th_prehisle.files.append(snk40th_prehisle_fgrom)
    snk40th_prehisle_spritesrom = SplitGameFile("PrehistoricIsleIn1930.sprites.rom", [("pi8910.k14")], 512 * 1024)
    snk40th_prehisle.files.append(snk40th_prehisle_spritesrom)
    snk40th_prehisle_spritesrom_2 = RenameGameFileOffset("PrehistoricIsleIn1930.sprites.rom", "gt5.5", 512 * 1024)
    snk40th_prehisle.files.append(snk40th_prehisle_spritesrom_2)
    snk40th_prehisle_bgmap = RenameGameFile("PrehistoricIsleIn1930.bg.map", "gt11.11")
    snk40th_prehisle.files.append(snk40th_prehisle_bgmap)
    snk40th_prehisle_samples = RenameGameFile("PrehistoricIsleIn1930.samples", "gt4.4")
    snk40th_prehisle.files.append(snk40th_prehisle_samples)
    all_games.append(snk40th_prehisle)
    
    snk40th_prehisleu = Game("Prehistoric Isle in 1930 (US)", conversion_type_snk40th, "Main", "prehisleu")
    snk40th_prehisleu.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_prehisleu.files.append(SplitGameFileEvenOdd("PrehistoricIsleIn1930.u.68k", [("gt-u2.2h", "gt-u3.3h")], 128 * 1024))
    snk40th_prehisleu.files.append(snk40th_prehisle_z80)
    snk40th_prehisleu.files.append(snk40th_prehisle_walpharom)
    snk40th_prehisleu.files.append(snk40th_prehisle_bgrom)
    snk40th_prehisleu.files.append(snk40th_prehisle_fgrom)
    snk40th_prehisleu.files.append(snk40th_prehisle_spritesrom)
    snk40th_prehisleu.files.append(snk40th_prehisle_spritesrom_2)
    snk40th_prehisleu.files.append(snk40th_prehisle_bgmap)
    snk40th_prehisleu.files.append(snk40th_prehisle_samples)
    all_games.append(snk40th_prehisleu)
    
    snk40th_gensitou = Game("Genshi-Tou 1930's (Japan) - Prehistoric Isle in 1930", conversion_type_snk40th, "Main", "gensitou")
    snk40th_gensitou.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_gensitou.files.append(SplitGameFileEvenOdd("PrehistoricIsleIn1930.j.68k", [("gt-j2.2h", "gt-j3.3h")], 128 * 1024))
    snk40th_gensitou.files.append(snk40th_prehisle_z80)
    snk40th_gensitou.files.append(snk40th_prehisle_walpharom)
    snk40th_gensitou.files.append(snk40th_prehisle_bgrom)
    snk40th_gensitou.files.append(snk40th_prehisle_fgrom)
    snk40th_gensitou.files.append(snk40th_prehisle_spritesrom)
    snk40th_gensitou.files.append(snk40th_prehisle_spritesrom_2)
    snk40th_gensitou.files.append(snk40th_prehisle_bgmap)
    snk40th_gensitou.files.append(snk40th_prehisle_samples)
    all_games.append(snk40th_gensitou)
    
    snk40th_saskue = Game("Sasuke vs. Commander", conversion_type_snk40th, "Patch1", "sasuke")
    snk40th_saskue.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_saskue.files.append(SplitGameFile(snk40th_saskue.rom_name +".maincpu", ("sc1", "sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc8", "sc9", "sc10"), 2048))
    snk40th_saskue.files.append(SplitGameFile(snk40th_saskue.rom_name +".gfx1", ("mcs_c", "mcs_d"), 2048))
    snk40th_saskue.files.append(RenameGameFile(snk40th_saskue.rom_name +".proms", "sasuke.clr"))
    snk40th_saskue.files.append(RenameGameFile(snk40th_saskue.rom_name +".snk6502", "sc11"))
    all_games.append(snk40th_saskue)
    
    snk40th_searchar = Game("SAR - Search And Rescue", conversion_type_snk40th, "DLC1", "searchar")
    snk40th_searchar.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_searchar.files.append(SplitGameFileEvenOdd(snk40th_searchar.rom_name +".maincpu", [("bh.2", "bh.3")], 128 * 1024))
    snk40th_searchar_user1 = SplitGameFileEvenOdd(snk40th_searchar.rom_name +".user1", [("bhw.1", "bhw.4")], 128 * 1024)
    snk40th_searchar.files.append(snk40th_searchar_user1)
    snk40th_searchar_soundcpu = RenameGameFile(snk40th_searchar.rom_name +".soundcpu", "bh.5")
    snk40th_searchar.files.append(snk40th_searchar_soundcpu)
    snk40th_searchar_gfx1 = SplitGameFile(snk40th_searchar.rom_name +".gfx1", ("bh.7", "bh.8"), 32768)
    snk40th_searchar.files.append(snk40th_searchar_gfx1)
    snk40th_searchar_gfx2 = SplitGameFile(snk40th_searchar.rom_name +".gfx2", ("bh.c1", "bh.c3", "bh.c5",), 512 * 1024)
    snk40th_searchar.files.append(snk40th_searchar_gfx2)
    snk40th_searchar_gfx2_2 = SplitGameFileOffset(snk40th_searchar.rom_name +".gfx2", ("bh.c2", "bh.c4", "bh.c6"), 512 * 1024, 2097152)
    snk40th_searchar.files.append(snk40th_searchar_gfx2_2)
    snk40th_searchar_upd = RenameGameFile(snk40th_searchar.rom_name +".upd", "bh.v1")
    snk40th_searchar.files.append(snk40th_searchar_upd)
    all_games.append(snk40th_searchar)
    
    snk40th_searcharu = Game("SAR - Search And Rescue (US)", conversion_type_snk40th, "DLC1", "searcharu")
    snk40th_searcharu.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_searcharu.files.append(SplitGameFileEvenOdd(snk40th_searcharu.rom_name +".maincpu", [("bh.2", "bh.3")], 128 * 1024))
    snk40th_searcharu.files.append(SplitGameFileEvenOdd(snk40th_searcharu.rom_name +".user1", [("bh.1", "bh.4")], 128 * 1024))
    snk40th_searcharu.files.append(snk40th_searchar_soundcpu)
    snk40th_searcharu.files.append(snk40th_searchar_gfx1)
    snk40th_searcharu.files.append(snk40th_searchar_gfx2)
    snk40th_searcharu.files.append(snk40th_searchar_gfx2_2)
    snk40th_searcharu.files.append(snk40th_searchar_upd)
    all_games.append(snk40th_searcharu)
    
    snk40th_searcharj = Game("SAR - Search And Rescue (Japan)", conversion_type_snk40th, "DLC1", "searcharj")
    snk40th_searcharj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_searcharj.files.append(SplitGameFileEvenOdd(snk40th_searcharj.rom_name +".maincpu", [("bh2ver3j.9c", "bh2ver3j.10c")], 128 * 1024))
    snk40th_searcharj.files.append(snk40th_searchar_user1)
    snk40th_searcharj.files.append(snk40th_searchar_soundcpu)
    snk40th_searcharj.files.append(snk40th_searchar_gfx1)
    snk40th_searcharj.files.append(snk40th_searchar_gfx2)
    snk40th_searcharj.files.append(snk40th_searchar_gfx2_2)
    snk40th_searcharj.files.append(snk40th_searchar_upd)
    all_games.append(snk40th_searcharj)
    
    snk40th_streetsm = Game("Street Smart", conversion_type_snk40th, "Main", "streetsm")
    snk40th_streetsm.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_streetsm.files.append(SplitGameFileEvenOdd(snk40th_streetsm.rom_name +".maincpu", [("s2-1ver2.14h", "s2-1ver2.14k")], 128 * 1024))
    snk40th_streetsm_soundcpu = RenameGameFile(snk40th_streetsm.rom_name +".soundcpu", "s2-5.16c")
    snk40th_streetsm.files.append(snk40th_streetsm_soundcpu)
    snk40th_streetsm.files.append(SplitGameFile(snk40th_streetsm.rom_name +".gfx1", ("s2-9.25l", "s2-10.25m"), 32 * 1024))
    snk40th_streetsm_gfx2 = SplitGameFile(snk40th_streetsm.rom_name +".gfx2", ("stsmart.900", "stsmart.902", "stsmart.904"), 512 * 1024)
    snk40th_streetsm.files.append(snk40th_streetsm_gfx2)
    snk40th_streetsm_gfx2_2 = SplitGameFileOffset(snk40th_streetsm.rom_name +".gfx2", ("stsmart.901", "stsmart.903", "stsmart.905"), 512 * 1024, 2097152)
    snk40th_streetsm.files.append(snk40th_streetsm_gfx2_2)
    snk40th_streetsm_upd = RenameGameFile(snk40th_streetsm.rom_name +".upd", "s2-6.18d")
    snk40th_streetsm.files.append(snk40th_streetsm_upd)
    all_games.append(snk40th_streetsm)
    
    snk40th_streetsm1 = Game("Street Smart (Version 1)", conversion_type_snk40th, "Main", "streetsm1")
    snk40th_streetsm1.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_streetsm1.files.append(SplitGameFileEvenOdd(snk40th_streetsm1.rom_name +".maincpu", [("s2-1ver1.9c", "s2-1ver1.10c")], 128 * 1024))
    snk40th_streetsm1.files.append(snk40th_streetsm_soundcpu)
    snk40th_streetsm1_gfx1 = SplitGameFile(snk40th_streetsm1.rom_name +".gfx1", ("s2-7.15l", "s2-8.15m"), 32 * 1024)
    snk40th_streetsm1.files.append(snk40th_streetsm1_gfx1)
    snk40th_streetsm1.files.append(snk40th_streetsm_gfx2)
    snk40th_streetsm1.files.append(snk40th_streetsm_gfx2_2)
    snk40th_streetsm1.files.append(snk40th_streetsm_upd)
    all_games.append(snk40th_streetsm1)
    
    snk40th_streetsmw = Game("Street Smart (World)", conversion_type_snk40th, "Main", "streetsmw")
    snk40th_streetsmw.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_streetsmw.files.append(SplitGameFileEvenOdd(snk40th_streetsmw.rom_name +".maincpu", [("s-smart1.bin", "s-smart2.bin")], 128 * 1024))
    snk40th_streetsmw.files.append(snk40th_streetsm_soundcpu)
    snk40th_streetsmw.files.append(snk40th_streetsm1_gfx1)
    snk40th_streetsmw.files.append(snk40th_streetsm_gfx2)
    snk40th_streetsmw.files.append(snk40th_streetsm_gfx2_2)
    snk40th_streetsmw.files.append(snk40th_streetsm_upd)
    all_games.append(snk40th_streetsmw)
    
    snk40th_streetsmj = Game("Street Smart (Japan)", conversion_type_snk40th, "Main", "streetsmj")
    snk40th_streetsmj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_streetsmj.files.append(SplitGameFileEvenOdd(snk40th_streetsmj.rom_name +".maincpu", [("s2v1j_01.bin", "s2v1j_02.bin")], 128 * 1024))
    snk40th_streetsmj.files.append(snk40th_streetsm_soundcpu)
    snk40th_streetsmj.files.append(snk40th_streetsm1_gfx1)
    snk40th_streetsmj.files.append(snk40th_streetsm_gfx2)
    snk40th_streetsmj.files.append(snk40th_streetsm_gfx2_2)
    snk40th_streetsmj.files.append(snk40th_streetsm_upd)
    all_games.append(snk40th_streetsmj)
    
    snk40th_timesold = Game("Time Soldiers", conversion_type_snk40th, "Patch1", "timesold")
    snk40th_timesold.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_timesold.files.append(SplitGameFileEvenOdd("TimeSoldiers.3.68k", [("bf.3", "bf.4"), ("bf.1", "bf.2")], 64 * 1024))
    snk40th_timesold_z80 = SplitGameFile("TimeSoldiers.z80", ("bf.7", "bf.8", "bf.9"), 64 * 1024)
    snk40th_timesold.files.append(snk40th_timesold_z80)
    snk40th_timesold.files.append(SplitGameFileEvenOdd("TimeSoldiers.u.gfx1.rom", [("bf.6", "bf.5")], 32 * 1024))
    snk40th_timesold_gfx2 = SplitGameFile("TimeSoldiers.gfx2.rom", ("bf.10", "bf.14", "bf.18"), 128 * 1024)
    snk40th_timesold_gfx2_2 = SplitGameFileOffset("TimeSoldiers.gfx2.rom", ("bf.11", "bf.15", "bf.19"), 128 * 1024, 128 * 1024 * 4)
    snk40th_timesold_gfx2_3 = SplitGameFileOffset("TimeSoldiers.gfx2.rom", ("bf.12", "bf.16", "bf.20"), 128 * 1024, 128 * 1024 * 8)
    snk40th_timesold_gfx2_4 = SplitGameFileOffset("TimeSoldiers.gfx2.rom", ("bf.13", "bf.17", "bf.21"), 128 * 1024, 128 * 1024 * 12)
    snk40th_timesold.files.append(snk40th_timesold_gfx2)
    snk40th_timesold.files.append(snk40th_timesold_gfx2_2)
    snk40th_timesold.files.append(snk40th_timesold_gfx2_3)
    snk40th_timesold.files.append(snk40th_timesold_gfx2_4)
    all_games.append(snk40th_timesold)
    
    snk40th_btlfield = Game("Battle Field (Japan) - Time Soldiers", conversion_type_snk40th, "Patch1", "btlfield")
    snk40th_btlfield.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_btlfield.files.append(SplitGameFileEvenOdd("TimeSoldiers.j.68k", [("bfv1_03.bin", "bfv1_04.bin"), ("bf.1", "bf.2")], 64 * 1024))
    snk40th_btlfield.files.append(snk40th_timesold_z80)
    snk40th_btlfield.files.append(SplitGameFileEvenOdd("TimeSoldiers.j.gfx1.rom", [("bfv1_06.bin", "bfv1_05.bin")], 32 * 1024))
    snk40th_btlfield.files.append(snk40th_timesold_gfx2)
    snk40th_btlfield.files.append(snk40th_timesold_gfx2_2)
    snk40th_btlfield.files.append(snk40th_timesold_gfx2_3)
    snk40th_btlfield.files.append(snk40th_timesold_gfx2_4)
    all_games.append(snk40th_btlfield)
    
    snk40th_vanguard = Game("Vanguard", conversion_type_snk40th, "Main", "vanguard")
    snk40th_vanguard.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_vanguard.files.append(SplitGameFile(snk40th_vanguard.rom_name +".maincpu", ["sk4_ic07.bin", "sk4_ic08.bin", "sk4_ic09.bin", "sk4_ic10.bin", "sk4_ic13.bin", "sk4_ic14.bin", "sk4_ic15.bin", "sk4_ic16.bin"], 4096))
    snk40th_vanguard_gfx1 = SplitGameFile(snk40th_vanguard.rom_name +".gfx1", ["sk5_ic50.bin", "sk5_ic51.bin"], 2048)
    snk40th_vanguard.files.append(snk40th_vanguard_gfx1)
    snk40th_vanguard_proms = SplitGameFile(snk40th_vanguard.rom_name +".proms", ["sk5_ic7.bin", "sk5_ic6.bin"], 32)
    snk40th_vanguard.files.append(snk40th_vanguard_proms)
    snk40th_vanguard_snk6502 = SplitGameFile(snk40th_vanguard.rom_name +".snk6502", ["sk4_ic51.bin", "sk4_ic52.bin"], 2048)
    snk40th_vanguard.files.append(snk40th_vanguard_snk6502)
    snk40th_vanguard_speech = SplitGameFile(snk40th_vanguard.rom_name +".speech", ["hd38882.bin"], 16 * 1024)
    snk40th_vanguard.files.append(snk40th_vanguard_speech)
    snk40th_vanguard_speech_2 = SplitGameFileOffset(snk40th_vanguard.rom_name +".speech", ["sk6_ic07.bin", "sk6_ic08.bin", "sk6_ic11.bin"], 2048, 16 * 1024)
    snk40th_vanguard.files.append(snk40th_vanguard_speech_2)
    all_games.append(snk40th_vanguard)
    
    snk40th_vanguardc = Game("Vanguard (Centuri)", conversion_type_snk40th, "Main", "vanguardc")
    snk40th_vanguardc.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_vanguardc.files.append(SplitGameFile(snk40th_vanguardc.rom_name +".maincpu", ["sk4_ic07.bin", "sk4_ic08.bin", "sk4_ic09.bin", "4", "5", "sk4_ic14.bin", "sk4_ic15.bin", "8"], 4096))
    snk40th_vanguardc.files.append(snk40th_vanguard_gfx1)
    snk40th_vanguardc.files.append(snk40th_vanguard_proms)
    snk40th_vanguardc.files.append(snk40th_vanguard_snk6502)
    snk40th_vanguardc.files.append(snk40th_vanguard_speech)
    snk40th_vanguardc.files.append(snk40th_vanguard_speech_2)
    all_games.append(snk40th_vanguardc)
    
    snk40th_vanguardj = Game("Vanguard (Japan)", conversion_type_snk40th, "Main", "vanguardj")
    snk40th_vanguardj.compatibility.extend(["FB Neo, MAME untested"])
    snk40th_vanguardj.files.append(SplitGameFile(snk40th_vanguardj.rom_name +".maincpu", ["sk4_ic07.bin", "sk4_ic08.bin", "sk4_ic09.bin", "vgj4ic10.bin", "vgj5ic13.bin", "sk4_ic14.bin", "sk4_ic15.bin", "sk4_ic16.bin"], 4096))
    snk40th_vanguardj.files.append(snk40th_vanguard_gfx1)
    snk40th_vanguardj.files.append(snk40th_vanguard_proms)
    snk40th_vanguardj.files.append(snk40th_vanguard_snk6502)
    snk40th_vanguardj.files.append(snk40th_vanguard_speech)
    snk40th_vanguardj.files.append(snk40th_vanguard_speech_2)
    all_games.append(snk40th_vanguardj)
    
    samsho_samsho = Game("Samurai Shodown", conversion_type_samuraishowdowncollection, "Main", "samsho")
    samsho_samsho.compatibility.extend(["Nothing - Garbled Graphics"])
    samsho_samsho.files.append(RenameGameFileOffset(samsho_samsho.rom_name +".cslot1_audiocpu", "045-m1.m1", (192 * 1024) - (128 * 1024)))
    samsho_samsho.files.append(RenameGameFile(samsho_samsho.rom_name +".cslot1_fixed", "045-s1.s1"))
    samsho_samsho.files.append(SplitGameFile(samsho_samsho.rom_name +".cslot1_ymsnd", ["045-v1.v1", "045-v2.v2"], 2097152))
    samsho_samsho.files.append(SplitGameFileSwab(samsho_samsho.rom_name +".cslot1_maincpu", [("045-p1.p1"),("045-pg2.sp2")], 1048576))
    samsho_samsho.files.append(SplitGameFileSwab("SamuraiShodown_NGM.sprites.swizzled", ("045-c1.c1", "045-c2.c2", "045-c3.c3", "045-c4.c4"), 2097152))
    samsho_samsho.files.append(SplitGameFileSwabOffset("SamuraiShodown_NGM.sprites.swizzled", ("045-c51.c5", "045-c61.c6"), 1048576, 2097152 * 4))
    all_games.append(samsho_samsho)
    
    samsho_samsho2 = Game("Samurai Shodown II", conversion_type_samuraishowdowncollection, "Main", "samsho2")
    samsho_samsho2.compatibility.extend(["Nothing - Garbled Graphics, Broken 063-p1.p1 file."])
    samsho_samsho2.files.append(RenameGameFileOffset(samsho_samsho2.rom_name +".cslot1_audiocpu", "063-m1.m1", (192 * 1024) - (128 * 1024))) #Perfect
    samsho_samsho2.files.append(RenameGameFile(samsho_samsho2.rom_name +".cslot1_fixed", "063-s1.s1")) #Perfect
    samsho_samsho2.files.append(SplitGameFile(samsho_samsho2.rom_name +".cslot1_ymsnd", ["063-v1.v1", "063-v2.v2", "063-v3.v3"], 2097152)) #Perfect
    samsho_samsho2.files.append(RenameGameFileOffset(samsho_samsho2.rom_name +".cslot1_ymsnd", "063-v4.v4", 2097152 * 3)) #Perfect
    samsho_samsho2.files.append(RenameGameFile(samsho_samsho2.rom_name +".cslot1_maincpu", "063-p1.p1"))
    samsho_samsho2.files.append(SplitGameFileSwab("SamuraiShodown2_NGM.sprites.swizzled", ("063-c1.c1", "063-c2.c2", "063-c3.c3", "063-c4.c4", "063-c5.c5", "063-c6.c6", "063-c7.c7", "063-c8.c8"), 2097152))
    all_games.append(samsho_samsho2)
    
    samsho_samsho2k = Game("Samurai Shodown II", conversion_type_samuraishowdowncollection, "Main", "samsho2k")
    samsho_samsho2k.compatibility.extend(["Nothing - Garbled Graphics, Missing Files."])
    samsho_samsho2k.files.append(RenameGameFileOffset(samsho_samsho2.rom_name +".cslot1_audiocpu", "063-m1.m1", (192 * 1024) - (128 * 1024))) #Perfect
    samsho_samsho2k.files.append(RenameGameFile(samsho_samsho2.rom_name +".cslot1_fixed", "063-s1.s1")) #Perfect
    samsho_samsho2k.files.append(SplitGameFile(samsho_samsho2.rom_name +".cslot1_ymsnd", ["063-v1.v1", "063-v2.v2", "063-v3.v3"], 2097152)) #Perfect
    samsho_samsho2k.files.append(RenameGameFileOffset(samsho_samsho2.rom_name +".cslot1_ymsnd", "063-v4.v4", 2097152 * 3)) #Perfect
    samsho_samsho2k.files.append(SplitGameFileSwabOffset(samsho_samsho2.rom_name +".cslot1_maincpu", ["063-ep2-kan.ep2"], 524288, 524288)) #perfect
    samsho_samsho2k.files.append(SplitGameFileSwab("SamuraiShodown2_NGM.sprites.swizzled", ("063-c1.c1", "063-c2.c2", "063-c3.c3", "063-c4.c4", "063-c5.c5", "063-c6.c6", "063-c7.c7", "063-c8.c8"), 2097152))
    all_games.append(samsho_samsho2k)
    
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
            
def rename_file_offset(src_path, dst_dir, file):
    with open(src_path, "rb") as src:
        src.read(file.offset)
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
    with zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED) as zipObj:
        for folderName, subfolders, filenames in os.walk(zipdir):
            for filename in filenames:
                zipfileLocation=(zipdir+'/'+filename)
                zipObj.write(zipfileLocation, filename)
    print(game.name + " has been zipped to " +zipname)
    
def unzip_game(root_dir, game):
    zipname=root_dir+'/'+game.extracted_folder_name+'.zip'
    if os.path.exists(zipname) == False :
        print_if_debug("File not found: " +zipname)
        return False
    gamedir=root_dir+'/'+game.extracted_folder_name
    with zipfile.ZipFile(zipname, 'r') as zipObj:
        zipObj.extractall(gamedir)
    print_if_debug(game.extracted_folder_name +".zip has been unzipped to " +gamedir)

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
            print_if_debug("File not found: " +src_path)
            return False
            
def get_string_rom_name_list(games) :
    gameNames = []
    for game in games :
        gameNames.append(game.rom_name)
    return ", ".join(gameNames)

def check_overwrite(rom_dir, game, overwrite) :
    if overwrite == False :
        rom_file_name = rom_dir+'/'+game.rom_name+'.zip'
        print_if_debug("rom_file_name: " +rom_file_name)
        if os.path.exists(rom_file_name) == True :
            print(game.name +" already converted.")
            game.converted = True
            return False
            
    return True
    
def check_zip_exists_if_necessary(root_dir, game):
    if "zip" in game.extracted_folder_name :
        game.extracted_folder_name = game.extracted_folder_name.replace(".zip", "")
        if unzip_game(root_dir,game) == False :
            print("Unable to extract " +game.name  +" (" +game.contained_within +"). Reason:  Zip file not found.")
            return False

def process_game_list(root_dir, game_list, rom_dir, overwrite):
    for game in game_list:
        print_if_debug("Overwrite: " +str(overwrite))
        if check_overwrite(rom_dir, game, overwrite) == False :
            continue
        if check_zip_exists_if_necessary(root_dir, game) == False :
            continue
        if check_files_exist(root_dir, game) == False:
            print("Unable to extract " +game.name  +" (" +game.contained_within +"). Reason:  One or more files not found.")
            continue
        print("Converting: " +game.name)
        for file in game.files:
            src_path = os.path.join(root_dir, game.extracted_folder_name, file.filename)
            dst_dir = os.path.join(rom_dir, game.rom_name)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            if isinstance(file, SplitGameFile):
                split_file(src_path, dst_dir, file)
            if isinstance(file, SplitGameFileOffset):
                split_file_offset(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileEvenOdd):
                split_file_evenodd(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileEvenOddOffset) :
                split_file_evenodd_offset(src_path, dst_dir, file)
            elif isinstance(file, RenameGameFile):
                rename_file(src_path, dst_dir, file)
            elif isinstance(file, RenameGameFileOffset):
                rename_file_offset(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileInterleave4Cps1) :
                split_file_interleave_4_cps1(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileSwab) :
                split_file_swab(src_path, dst_dir, file)
            elif isinstance(file, SplitGameFileSwabOffset) :
                split_file_swab_offset(src_path, dst_dir, file)
        zip_game(rom_dir, game)
        if len(game.compatibility) > 0 :
            print(game.name +" is compatible with " + ", ".join(game.compatibility))
        game.converted = True
        rm_dir(rom_dir+'/'+game.rom_name)

def begin_convert(root_dir, rom_dir, rom_name, conversion_type, all_games, overwrite):
    #create rom_dir if missing
    if not os.path.exists(rom_dir):
        os.mkdir(rom_dir)
        
    game_list = create_game_list(rom_name, conversion_type, all_games)
    process_game_list(root_dir, game_list, rom_dir, overwrite)
    end_convert(game_list, overwrite)

def end_convert(game_list, overwrite) :
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
    if overwrite == False :
        print(str(successful) +"/" +str(total) +" converted successfully (or already exist).")
    else :
        print(str(successful) +"/" +str(total) +" converted successfully.")
    if unsuccessful > 0 :
        print("Unsuccessful:")
        print("\n".join(unsuccessfulList))
        

def main(argc, argv):
    all_games = get_games()
    if argc < 3:
        usage(get_string_rom_name_list(all_games))

    parser = argparse.ArgumentParser()
    parser.add_argument("extractFolderStr", help="Location for extraction", type=str)
    parser.add_argument("romFolderStr", help="Location for rom", type=str)
    parser.add_argument("--rom", "--r", help="rom name", type=str)
    parser.add_argument("--type", "--t", help="conversion type", type=str)
    parser.add_argument('--debug', "--d", "--v", help="enable debug", action='store_true', default=False)
    parser.add_argument('--overwrite', "--o", help="enable debug", action='store_true', default=False)
    args = parser.parse_args()

    root_dir = args.extractFolderStr
    rom_dir = args.romFolderStr
    rom_name = args.rom
    conversion_type = args.type
    global debug
    debug = args.debug
    overwrite = args.overwrite
    
    begin_convert(root_dir, rom_dir, rom_name, conversion_type, all_games, overwrite)

    exit(0)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
        