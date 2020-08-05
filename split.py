import os
import sys
import argparse
from zipfile import ZipFile

def usage():
    print("Usage: python split.py \"...ExtractionFolder...\" \"...RomFolder...\" \"RomName\"")
    sys.exit(0)

##################################################################################################################
#Streetfighter
#code (maincpu-u.68k)
#gfx (gfx1-bplanes.rom 0-3, gfx2-mplanes.rom 0-3, gfx3-sprites.rom 0-3, gfx4-alpha.rom, tilerom-maps.rom)
#files (audiocpu-z80, audio2-samples.rom)
sf_code = [(
    [
        ("sfd-19.2a", "sfd-22.2c"),
        ("sfd-20.3a", "sfd-23.3c"),
        ("sfd-21.4a", "sfd-24.4c")
    ],
    "u.68k",
    64 * 1024
)]

sf_files = [
    (["sf-39.2k", "sf-38.1k", "sf-41.4k", "sf-40.3k"], "bplanes.rom", 128 * 1024),
    (["sf-25.1d", "sf-28.1e", "sf-30.1g", "sf-34.1h", "sf-26.2d", "sf-29.2e", "sf-31.2g", "sf-35.2h"], "mplanes.rom", 128 * 1024),
    (["sf-15.1m", "sf-16.2m", "sf-11.1k", "sf-12.2k", "sf-07.1h", "sf-08.2h", "sf-03.1f", "sf-17.3m", "sf-18.4m", "sf-13.3k", "sf-14.4k", "sf-09.3h", "sf-10.4h","sf-05.3f"], "sprites.rom", 128 * 1024),
    (["sf-27.4d"], "alpha.rom", 16 * 1024),
    (["sf-37.4h", "sf-36.3h", "sf-32.3g", "sf-33.4g"], "maps.rom", 64 * 1024),
    (["sf-02.7k"], "z80", 32 * 1024),
    (["sfu-00.1h", "sf-01.1k"], "u.samples.rom", 128 * 1024)
]

##################################################################################################################
#Streetfighter II
#code (maincpu-ub.68k)
#gfx (vrom)
#files (audiocpu-z80, samples-oki)
sf2ub_code = [(
    [
        ("sf2u.30e", "sf2u.37e"),
        ("sf2u.31e", "sf2u.38e"),
        ("sf2u.28e", "sf2u.35e"),
        ("sf2.29a", "sf2.36a")
    ],
    "ub.68k",
    128 * 1024
)]

sf2ub_gfx = [(
    [
        ("sf2_06.bin", "sf2_08.bin", "sf2_05.bin", "sf2_07.bin"),
        ("sf2_15.bin", "sf2_17.bin", "sf2_14.bin", "sf2_16.bin"),
        ("sf2_25.bin", "sf2_27.bin", "sf2_24.bin", "sf2_26.bin")
    ],
    "vrom",
    512 * 1024
)]
#bank size is 0x80000

sf2ub_files = [
    (["sf2_09.bin"], "z80", 64 * 1024),
    (["sf2_18.bin", "sf2_19.bin"], "oki", 128 * 1024),
]

##################################################################################################################
#Streetfighter II': Champion Edition
#code (maincpu-ua.68k)
#gfx (vrom)
#files (audiocpu-z80, samples-oki)
sf2ceua_code = [(
    [
        ("s92u-23a"),
        ("sf2ce.22"),
        ("s92_21a.bin")
    ],
    "ua.68k",
    512 * 1024
)]
#bank size is 0x80000

sf2ceua_gfx = [(
    [
        ("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),
        ("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),
        ("s92_10.bin", "s92_11.bin", "s92_12.bin", "s92_13.bin")
    ],
    "vrom",
    512 * 1024
)]
#bank size is 0x80000

sf2ceua_files = [
    (["s92_09.bin"], "z80", 64 * 1024),
    (["s92_18.bin", "s92_19.bin"], "oki", 128 * 1024),
]

##################################################################################################################
#StreetFighter II': Hyper Fighting (1992)
#code (maincpu-ua.68k)
#gfx (vrom)
#files (audiocpu-z80, samples-oki)
sf2t_code = [(
    [
        ("sf2_23"),
        ("sf2_22.bin"),
        ("sf2_21.bin")
    ],
    "u.68k",
    512 * 1024
)]
#bank size is 0x80000

sf2t_gfx = [(
    [
        ("s92_01.bin", "s92_02.bin", "s92_03.bin", "s92_04.bin"),
        ("s92_05.bin", "s92_06.bin", "s92_07.bin", "s92_08.bin"),
        ("s2t_10.bin", "s2t_11.bin", "s2t_12.bin", "s2t_13.bin")
    ],
    "u.vrom",
    512 * 1024
)]
#bank size is 0x80000

sf2t_files = [
    (["s92_09.bin"], "z80", 64 * 1024),
    (["s92_18.bin", "s92_19.bin"], "oki", 128 * 1024),
]

##################################################################################################################
#Super StreetFighter II (1993)
#code (maincpu-ua.68k)
#gfx (vrom)
#files (audiocpu-z80, samples-oki)
ssf2u_code = [(
    [
        ("ssfu.03a"),
        ("ssfu.04a"),
        ("ssfu.05"),
        ("ssfu.06"),
        ("ssfu.07")
    ],
    "u.68k",
    512 * 1024
)]
#bank size is 0x80000

ssf2u_gfx = [(
    [
        ("ssf.13m", "ssf.15m", "ssf.17m", "ssf.19m"),
        ("ssf.14m", "ssf.16m", "ssf.18m", "ssf.20m")
    ],
    "vrom",
    2048 * 1024
)]

#bank size is 0x80000

ssf2u_files = [
    (["ssf.01"], "z80", 64 * 1024),
    (["ssf.q01", "ssf.q01", "ssf.q03", "ssf.q04", "ssf.q05", "ssf.q06", "ssf.q07", "ssf.q08"], "qs", 128 * 1024),
]

##################################################################################################################
sfiii_files = [
    (["sfiii-simm1.0", "sfiii-simm1.1", "sfiii-simm1.2", "sfiii-simm1.3"], "s1", 2097152),
    (["sfiii-simm3.0", "sfiii-simm3.1", "sfiii-simm3.2", "sfiii-simm3.3", "sfiii-simm3.4", "sfiii-simm3.5", "sfiii-simm3.6", "sfiii-simm3.7"], "s3", 2097152),
    (["sfiii-simm4.0", "sfiii-simm4.1", "sfiii-simm4.2", "sfiii-simm4.3", "sfiii-simm4.4", "sfiii-simm4.5", "sfiii-simm4.6", "sfiii-simm4.7"], "s4", 2097152),
    (["sfiii-simm5.0", "sfiii-simm5.1", "sfiii-simm5.2", "sfiii-simm5.3", "sfiii-simm5.4", "sfiii-simm5.5", "sfiii-simm5.6", "sfiii-simm5.7"], "s5", 2097152),
    (["sfiii_euro.29f400.u2"], "bios", 512 * 1024)
]

sfiii2_files = [
    (["sfiii2-simm1.0", "sfiii2-simm1.1", "sfiii2-simm1.2", "sfiii2-simm1.3"], "s1", 2097152),
    (["sfiii2-simm2.0", "sfiii2-simm2.1", "sfiii2-simm2.2", "sfiii2-simm2.3"], "s2", 2097152),
    (["sfiii2-simm3.0", "sfiii2-simm3.1", "sfiii2-simm3.2", "sfiii2-simm3.3", "sfiii2-simm3.4", "sfiii2-simm3.5", "sfiii2-simm3.6", "sfiii2-simm3.7"], "s3", 2097152),
    (["sfiii2-simm4.0", "sfiii2-simm4.1", "sfiii2-simm4.2", "sfiii2-simm4.3", "sfiii2-simm4.4", "sfiii2-simm4.5", "sfiii2-simm4.6", "sfiii2-simm4.7"], "s4", 2097152),
    (["sfiii2-simm5.0", "sfiii2-simm5.1", "sfiii2-simm5.2", "sfiii2-simm5.3", "sfiii2-simm5.4", "sfiii2-simm5.5", "sfiii2-simm5.6", "sfiii2-simm5.7"], "s5", 2097152),
    (["sfiii2_usa.29f400.u2"], "bios", 512 * 1024)
]

sfiii3_files = [
    (["sfiii3-simm1.0", "sfiii3-simm1.1", "sfiii3-simm1.2", "sfiii3-simm1.3"], "r1.s1", 2097152),
    (["sfiii3-simm2.0", "sfiii3-simm2.1", "sfiii3-simm2.2", "sfiii3-simm2.3"], "r1.s2", 2097152),
    (["sfiii3-simm3.0", "sfiii3-simm3.1", "sfiii3-simm3.2", "sfiii3-simm3.3", "sfiii3-simm3.4", "sfiii3-simm3.5", "sfiii3-simm3.6", "sfiii3-simm3.7"], "s3", 2097152),
    (["sfiii3-simm4.0", "sfiii3-simm4.1", "sfiii3-simm4.2", "sfiii3-simm4.3", "sfiii3-simm4.4", "sfiii3-simm4.5", "sfiii3-simm4.6", "sfiii3-simm4.7"], "s4", 2097152),
    (["sfiii3-simm5.0", "sfiii3-simm5.1", "sfiii3-simm5.2", "sfiii3-simm5.3", "sfiii3-simm5.4", "sfiii3-simm5.5", "sfiii3-simm5.6", "sfiii3-simm5.7"], "s5", 2097152),
    (["sfiii3-simm6.0", "sfiii3-simm6.1", "sfiii3-simm6.2", "sfiii3-simm6.3", "sfiii3-simm6.4", "sfiii3-simm6.5", "sfiii3-simm6.6", "sfiii3-simm6.7"], "s6", 2097152),
    (["sfiii3_usa.29f400.u2"], "bios", 512 * 1024)
]

def zip_game(rom_dir, rom_name):
    zipname=rom_dir+'/'+rom_name+'.zip'
    zipdir=rom_dir+'/'+rom_name
    zipObj = ZipFile(zipname, 'w')
    for folderName, subfolders, filenames in os.walk(zipdir):
        for filename in filenames:
            # Add file to zip
            zipfile=(zipdir+'/'+filename)
            zipObj.write(zipfile)
            print('Added '+filename+' to '+zipname)

def rm_dir(dir):
    for folderName, subfolders, filenames in os.walk(dir):
        for filename in filenames:
            os.remove(folderName+'/'+filename)
        os.rmdir(folderName)

def split_code_file(dst_dir, dst_names, src_path, size):
    with open(src_path, "rb") as src:
        print(src_path)
        for (dst_even_name, dst_odd_name) in dst_names:
            print("\t" + dst_even_name + ", " + dst_odd_name)
            dst_even_path = os.path.join(dst_dir, dst_even_name)
            dst_odd_path = os.path.join(dst_dir, dst_odd_name)
            with open(dst_even_path, "wb") as dst_even:
                with open(dst_odd_path, "wb") as dst_odd:
                    for i in range(size):
                        dst_even.write(src.read(1))
                        dst_odd.write(src.read(1))

def split_code_file_alt(dst_dir, dst_names, src_path, size):
    with open(src_path, "rb") as src:
        print(src_path)
        print(dst_names)
        for (dst_name) in dst_names:
            print("\t" + dst_name)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                for i in range(size // 2):
                    byte0=src.read(1)
                    byte1=src.read(1)
                    dst.write(byte1)
                    dst.write(byte0)

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


def split_gfx_file(dst_dir, dst_names, src_path, size, type):
    with open(src_path, "rb") as src:
        print(src_path)
        if type == "cps1":
            print("Decoding CPS1 Graphics")
        for (dst_name_1, dst_name_2, dst_name_3, dst_name_4) in dst_names:
            print("\t" + dst_name_1 + ", " + dst_name_2 + ", " + dst_name_3 + ", " + dst_name_4)
            dst_path_1 = os.path.join(dst_dir, dst_name_1)
            dst_path_2 = os.path.join(dst_dir, dst_name_2)
            dst_path_3 = os.path.join(dst_dir, dst_name_3)
            dst_path_4 = os.path.join(dst_dir, dst_name_4)
            with open(dst_path_1, "wb") as dst_1:
                with open(dst_path_2, "wb") as dst_2:
                    with open(dst_path_3, "wb") as dst_3:
                        with open(dst_path_4, "wb") as dst_4:
                            for i in range(size // 2):
                                if type == "cps1":
                                    data = decode_cps1_gfx(src.read(8))
                                    dst_1.write(data[0:2])
                                    dst_2.write(data[2:4])
                                    dst_3.write(data[4:6])
                                    dst_4.write(data[6:8])
                                else:
                                    dst_1.write(src.read(2))
                                    dst_2.write(src.read(2))
                                    dst_3.write(src.read(2))
                                    dst_4.write(src.read(2))

def split_gfx_file_alt(dst_dir, dst_names, src_path, size, type, offset):
    with open(src_path, "rb") as src:
        print(src_path)
        src.read(offset)
        if type == "cps1":
            print("Decoding CPS1 Graphics")
        for (dst_name_1, dst_name_2, dst_name_3, dst_name_4) in dst_names:
            print("\t" + dst_name_1 + ", " + dst_name_2 + ", " + dst_name_3 + ", " + dst_name_4)
            dst_path_1 = os.path.join(dst_dir, dst_name_1)
            dst_path_2 = os.path.join(dst_dir, dst_name_2)
            dst_path_3 = os.path.join(dst_dir, dst_name_3)
            dst_path_4 = os.path.join(dst_dir, dst_name_4)
            with open(dst_path_1, "wb") as dst_1:
                with open(dst_path_2, "wb") as dst_2:
                    with open(dst_path_3, "wb") as dst_3:
                        with open(dst_path_4, "wb") as dst_4:
                            for i in range(size // 2):
                                if type == "cps1":
                                    data = decode_cps1_gfx(src.read(8))
                                    dst_1.write(data[0:2])
                                    dst_2.write(data[2:4])
                                    dst_3.write(data[4:6])
                                    dst_4.write(data[6:8])
                                else:
                                    dst_1.write(src.read(2))
                                    dst_2.write(src.read(2))
                                    dst_3.write(src.read(2))
                                    dst_4.write(src.read(2))

def split_file(dst_dir, dst_names, src_path, size):
    with open(src_path, "rb") as src:
        print(src_path)
        for dst_name in dst_names:
            print("\t" + dst_name)
            contents = src.read(size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)

def split_file_offset(dst_dir, dst_names, src_path, size, offset):
    with open(src_path, "rb") as src:
        print(src_path)
        src.read(offset)
        for dst_name in dst_names:
            print("\t" + dst_name)
            contents = src.read(size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)

#sf
def split_game(root_dir, rom_dir, rom_name, src_game_name, code_files, split_files, type):
    dst_dir = os.path.join(rom_dir, rom_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for (dst_names, src_ext, size) in code_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_code_file(dst_dir, dst_names, src_path, size)
    for (dst_names, src_ext, size) in split_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_file(dst_dir, dst_names, src_path, size)

#sf2ub,sfiiina,sfiii2n,sfiii3nr1
def split_game_alt1(root_dir, rom_dir, rom_name, src_game_name, code_files, gfx_files, split_files, type):
    dst_dir = os.path.join(rom_dir, rom_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    if type == "cps3":
        print("Splitting CPS3 Files")
        for (dst_names, src_ext, size) in split_files:
            src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
            split_file(dst_dir, dst_names, src_path, size)
    else:
        for (dst_names, src_ext, size) in code_files:
            src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
            split_code_file(dst_dir, dst_names, src_path, size)
        for (dst_names, src_ext, size) in gfx_files:
            src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
            split_gfx_file(dst_dir, dst_names, src_path, size, type)
        for (dst_names, src_ext, size) in split_files:
            src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
            split_file(dst_dir, dst_names, src_path, size)

#sf2hf
def split_game_alt2(root_dir, rom_dir, rom_name, src_game_name, code_files, gfx_files, split_files, type):
    dst_dir = os.path.join(rom_dir, rom_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for (dst_names, src_ext, size) in code_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_code_file_alt(dst_dir, dst_names, src_path, size)
    for (dst_names, src_ext, size) in gfx_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_gfx_file(dst_dir, dst_names, src_path, size, type)
    for (dst_names, src_ext, size) in split_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_file(dst_dir, dst_names, src_path, size)

def split_game_alt3(root_dir, rom_dir, rom_name, src_game_name, code_files, gfx1_files, gfx2_files, gfx2_offset, split_files, type):
    dst_dir = os.path.join(rom_dir, rom_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for (dst_names, src_ext, size) in code_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_code_file_alt(dst_dir, dst_names, src_path, size)
    for (dst_names, src_ext, size) in gfx1_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_gfx_file(dst_dir, dst_names, src_path, size, type)
    for (dst_names, src_ext, size) in gfx2_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_gfx_file_alt(dst_dir, dst_names, src_path, size, type, gfx2_offset)
    for (dst_names, src_ext, size) in split_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_file(dst_dir, dst_names, src_path, size)

def main(argc, argv):
    if argc != 4:
        usage()

    parser = argparse.ArgumentParser()
    parser.add_argument("extractFolderStr", help="Location for extraction", type=str)
    parser.add_argument("romFolderStr", help="Location for rom", type=str)
    parser.add_argument("romStr", help="rom name", type=str)

    args = parser.parse_args()

    root_dir = args.extractFolderStr
    rom_dir = args.romFolderStr
    rom_name = args.romStr

    if not os.path.exists(root_dir):
        print("Cant find extraction dir, are you sure you're using this correctly? Read the README.")
        exit(2)

    #create rom_dir if missing
    if not os.path.exists(rom_dir):
        os.mkdir(rom_dir)

    #remove rom_name subfolder if it exists
    if os.path.exists(rom_dir+'/'+rom_name):
        rm_dir(rom_dir+'/'+rom_name)

    #remove the rom_name.zip file if it exists
    if os.path.exists(rom_dir+'/'+rom_name+'.zip'):
        os.remove(rom_dir+'/'+rom_name+'.zip')

    #recreate an empty rom_name subfolder
    os.mkdir(rom_dir+'/'+rom_name)

    if rom_name=="sf":
        split_game(root_dir, rom_dir, rom_name, "StreetFighter", sf_code, sf_files, "cps1") # FB Neo
        zip_game(rom_dir, rom_name)
    elif rom_name=="sf2ub":
        split_game_alt1(root_dir, rom_dir, rom_name, "StreetFighterII", sf2ub_code, sf2ub_gfx, sf2ub_files, "cps1") # MAME-2003 Plus
        zip_game(rom_dir, rom_name)
    elif rom_name=="sf2ceua":
        split_game_alt2(root_dir, rom_dir, rom_name,  "StreetFighterII_CE", sf2ceua_code, sf2ceua_gfx, sf2ceua_files, "cps1")
        zip_game(rom_dir, rom_name)
    elif rom_name=="sf2t":
        split_game_alt2(root_dir, rom_dir, rom_name,  "StreetFighterII_HF", sf2t_code, sf2t_gfx, sf2t_files, "cps1")
        zip_game(rom_dir, rom_name)
    elif rom_name=="ssf2u":
        #gfx2_offset=0x800000
        split_game_alt1(root_dir, rom_dir, rom_name,  "SuperStreetFighterII", ssf2u_code, ssf2u_gfx, ssf2u_files, "cps2")
        zip_game(rom_dir, rom_name)
    elif rom_name=="ssf2tu":
        print("Unsupported rom="+rom_name)
    elif rom_name=="sfau":
        print("Unsupported rom="+rom_name)
    elif rom_name=="sfa2u":
        print("Unsupported rom="+rom_name)
    elif rom_name=="sfa3u":
        print("Unsupported rom="+rom_name)
    elif rom_name=="sfiiiu":
        split_game_alt1(root_dir, rom_dir, rom_name,  "StreetFighterIII", None, None, sfiii_files, "cps3")
        zip_game(rom_dir, rom_name)
    elif rom_name=="sfiii2":
        split_game_alt1(root_dir, rom_dir, rom_name,  "StreetFighterIII_2ndImpact", None, None, sfiii2_files, "cps3")
        zip_game(rom_dir, rom_name)
    elif rom_name=="sfiii3ur1":
        split_game_alt1(root_dir, rom_dir, rom_name,  "StreetFighterIII_3rdStrike", None, None, sfiii3_files, "cps3")
        zip_game(rom_dir, rom_name)
    else:
        print("Unsupported rom="+rom_name)

    print("Finished")

    exit(0)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
