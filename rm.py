#!/usr/bin/env python3

import argparse
import os
import shutil

TRASH = os.path.expanduser("~") + "/.trash/"

def write_log(trash_path, orig_path):
    with open(TRASH + "TRASH_LOG.log", "a") as f:
        f.write(TRASH + trash_path + "\n" + orig_path + "\n")


def authenticate_path(file_to_rm):
        file_full = os.path.abspath(file_to_rm)
        file_name = os.path.split(file_full)[-1]
        dest_file_full = file_full
        dest_file_name = file_name
        # same name exists in trash
        if os.path.exists(TRASH + file_name):
            count = 0
            # find which number makes this a unique value
            while (os.path.exists(TRASH + file_name + "." + str(count))):
                count += 1
            dest_file_name += "." + str(count)
            dest_file_full += "." + str(count)

        return file_full, dest_file_full, file_name, dest_file_name


def recur(base, perm):
    if perm:
        shutil.rmtree(base)
    else:
        dir_full, dest_dir_full, dir_name, dest_dir_name = authenticate_path(base)
        shutil.move(dir_full, TRASH + dest_dir_name)
        write_log(dest_dir_name, dir_full)
        

def single(file_to_rm, perm):
    if not os.path.isfile(file_to_rm):
        print("Not a regular file!")
        return
    if perm:
        os.remove(file_to_rm)
    else:
        file_full, dest_file_full, file_name, dest_file_name = authenticate_path(file_to_rm)
        shutil.move(file_full, TRASH + dest_file_name)
        write_log(dest_file_name, file_full)
        




def clean():
    recur(TRASH, True)
    os.mkdir(TRASH)
    f = open(TRASH + "TRASH_LOG.log", "w+")
    f.close()


def undo_delete():
    pairs = []
    with open(TRASH + "TRASH_LOG.log", "r") as log:
        for line in log:
            pairs.append(line.strip())

    # make sure there is value to restore
    if len(pairs) < 1:
        print("Your trash is empty.")
        return

    # to_restore = [trash, dest]
    to_restore = []
    to_restore.append(pairs[-2])
    to_restore.append(pairs[-1])
    if os.path.exists(to_restore[1]):
        print("There will be a name error; resolve the conflict in the destination.")
        return
    else:
        shutil.move(to_restore[0], to_restore[1])
        
        pairs = pairs[0:-2]
        with open(TRASH + "TRASH_LOG.log", "w") as log:
            # all but the last
            for p in pairs:
                log.write(p + "\n")


parser = argparse.ArgumentParser()
remove_vs_clean = parser.add_mutually_exclusive_group()
remove_vs_clean.add_argument("file", help="Remove FILE to ~/.trash.", 
       metavar="FILE", nargs="*", action="append", default=[])
remove_vs_clean.add_argument("-r", "--recursive", help="Remove directory to ~/.trash.", 
        metavar="DIR", nargs="*", action="append", default=[])
remove_vs_clean.add_argument("-e", "--empty-trash", help="Empty ~/.trash.", action="store_true")
remove_vs_clean.add_argument("-u", "--undo", help="Undo last delete.", action="store_true")
parser.add_argument("--permanent", help="Permanently delete file or directory.", action="store_true")

args = parser.parse_args()


# verify that the trash exists
if not os.path.exists(TRASH):
    os.mkdir(TRASH)
if not os.path.exists(TRASH + "TRASH_LOG.log"):
    f = open(TRASH + "TRASH_LOG.log", "w")
    f.close()

# parse the arguments
if args.recursive:
    for arg in args.recursive[0]:  # not sure why, but args.recursive is 2d
        recur(arg, args.permanent)

if args.file:
    for arg in args.file[0]:  # again; not sure why, but args.file is 2d
        single(arg, args.permanent)

if args.empty_trash:
    clean()

if args.undo:
    undo_delete()

