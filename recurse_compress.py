#!/usr/bin/env python3

""" Recurse and Compress """
from os import path, listdir
from shutil import rmtree
from sys import argv
from sys import exit as sysexit
from py7zr import SevenZipFile

if len(argv) != 2:
    print("Invalid Argument: Too many/few arguments passed. One needed.")
    sysexit(1)

dir_path = argv[1]

if path.exists(dir_path) != True:
    print("Invalid Argument: File/Directory doesn't exist.")
    sysexit(1)

if path.isdir(dir_path) != True:
    print("Invalid Argument: Must be a directory, not a file.")
    sysexit(1)

if path.isdir(path.dirname(path.abspath(dir_path))+"/"+dir_path) != True:
    dir_path_full = dir_path

if path.isdir(path.dirname(path.abspath(dir_path))+"/"+dir_path) == True:
    dir_path_full = path.dirname(path.abspath(dir_path))+"/"+dir_path

def list_full_paths(directory):
    """ list only the subdirectories in an directory """
    only_dirs = []
    for item in [path.join(directory, file) for file in listdir(directory)]:
        if path.isdir(item) == True:
            only_dirs.append(item)
    return only_dirs

def compress_directories(directory_list):
    """ compress each directory to 7z archive """
    success_list = []
    for dirs in directory_list:
        try:
            print("Archiving: "+dirs+".7z")
            with SevenZipFile(dirs+".7z", 'w') as archive:
                archive.writeall(dirs)
            success_list.append(dirs)
        except:
            print("Error: "+dirs)
    return success_list

sub_dir_list = list_full_paths(dir_path_full)

for subdirs in sub_dir_list:
    sub_subdir_list = list_full_paths(subdirs)
    if sub_subdir_list:
        success_compress = compress_directories(sub_subdir_list)

        for subdirs in success_compress:
            print("Removing: "+subdirs)
            rmtree(subdirs)
