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


def split_gfx_file(dst_dir, dst_names, src_path, size):
    with open(src_path, "rb") as src:
        print(src_path)
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


def split_game(dst_game_name, src_game_name, code_files, gfx_files, split_files):
    dst_dir = os.path.join(root_dir, dst_game_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for (dst_names, src_ext, size) in code_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_code_file(dst_dir, dst_names, src_path, size)
    for (dst_names, src_ext, size) in gfx_files:
        src_path = os.path.join(root_dir, src_game_name, src_game_name + "." + src_ext)
        split_gfx_file(dst_dir, dst_names, src_path, size)
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

split_game("sf2ub", "StreetFighterII", sf2_code, sf2_gfx, sf2_files)
