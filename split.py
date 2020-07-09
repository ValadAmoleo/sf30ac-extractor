import os
import sys

if len(sys.argv) != 2:
    print("Usage: python split.py \"C:\\...your extraction folder...\"")
    exit(1)

root_dir = sys.argv[1]

if not os.path.exists(root_dir):
    print("Cant find extraction dir, are you sure you're using this correctly? Read the README.")
    exit(2)


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

def split_file(dst_dir, dst_names, src_path, size):
    with open(src_path, "rb") as src:
        print(src_path)
        for dst_name in dst_names:
            print("\t" + dst_name)
            contents = src.read(size)
            dst_path = os.path.join(dst_dir, dst_name)
            with open(dst_path, "wb") as dst:
                dst.write(contents)


def split_game(dst_game_name, src_game_name, code_files, gfx_files, split_files, type):
    dst_dir = os.path.join(root_dir, dst_game_name)
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


sf2_code = [(
    [
        ("sf2u_30b.11e", "sf2u_37b.11f"),
        ("sf2u_31b.12e", "sf2u_38b.12f"),
        ("sf2u_28b.9e", "sf2u_35b.9f"),
        ("sf2_29b.10e", "sf2_36b.10f"),
    ],
    "ub.68k",
    128 * 1024
)]

sf2_gfx = [(
    [
        ("sf2-5m.4a", "sf2-7m.6a", "sf2-1m.3a", "sf2-3m.5a"),
        ("sf2-6m.4c", "sf2-8m.6c", "sf2-2m.3c", "sf2-4m.5c"),
        ("sf2-13m.4d", "sf2-15m.6d", "sf2-9m.3d", "sf2-11m.5d"),
    ],
    "vrom",
    512 * 1024
)]

sf2_files = [
    (["sf2_9.12a"], "z80", 64 * 1024),
    (["sf2_18.11c", "sf2_19.12c"], "oki", 128 * 1024),
]

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

split_game("sf2ua", "StreetFighterII", sf2_code, sf2_gfx, sf2_files, "cps1")
split_game("sfiiina", "StreetFighterIII", None, None, sfiii_files, "cps3")
split_game("sfiii2n", "StreetFighterIII_2ndImpact", None, None, sfiii2_files, "cps3")
split_game("sfiii3nr1", "StreetFighterIII_3rdStrike", None, None, sfiii3_files, "cps3")
