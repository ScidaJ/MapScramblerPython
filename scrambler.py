import argparse
import random
from io import TextIOWrapper
from os import getcwd
from os.path import exists
from pathlib import Path
from sys import exit

DIR = getcwd()
MAP_LIST_DIR_PATH = '\out'
MAP_LIST_PATH = '\maps.txt'

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('MapList', help='Path to the map list that you want to use with the scrambler. Will not create if it does not exist.')
    parser.add_argument('--ServerFile', help='Path to the server startup file or the file which contains the map list. Will not create if it does not exist. Do not use with --list.')
    parser.add_argument('--PreArg', help='Arguments that go before the map list. Spaces/New lines will not be added to the end.')
    parser.add_argument('--PostArg', help='Arguments that go after the map list. Spaces/New lines will not be added to the front.')
    parser.add_argument('--ArgSliceChar', help='Character to slice the server arguments by. Must be exactly 2 slice characters in server file, One directly before the map list, and one directly after. CANNOT be used with --PreArg or --PostArg.')
    parser.add_argument('-l', '--list', help='Enables output to a seperate list file instead of overwriting server file. Will be placed in \out\map_list.txt. Do not use with --ServerFile', action='store_true')
    parser.add_argument('-p', '--prefix', help='Prefix for map names. Space will not be added if they exist. E.g. mp [mapName]')
    parser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')

    args = parser.parse_args()

    validate_args(args)

    maps = {}
    map_list = {}
    final_map_file = None
    map_string = ''
    map_file = open(args.MapList, 'r').read()
    map_file = map_file.split('\n')
    size = len(map_file)

    server_file_exists = False

    if args.ServerFile is not None:
        server_file_exists = exists(args.ServerFile)
    for curr_map in map_file:
        curr_map = curr_map.split(',')
        maps[curr_map[1]] = curr_map[0]
        index = random.randint(0, size)
        while index in map_list:
            index = random.randint(0, size)
        map_list[index] = curr_map[1]
    print('Maps have been scrambled, writing to ', 'server file' if args.list is None else 'list file')
    if (args.ServerFile is not None and not server_file_exists) and args.list is None:
        print('Your server file', args.ServerFile, 'does not exist. Creating the file now.')
        final_map_file = open(args.ServerFile, 'rw')
    else:
        print('Creating directory and map list file if it does not exist.' if args.list else 'You have not specified a server file or set list file argument, defaulting to list file.')
        args.ServerFile = None
        Path(f'{DIR}{MAP_LIST_DIR_PATH}').mkdir(parents=True, exist_ok=True)
        final_map_file = open(f'{DIR}{MAP_LIST_DIR_PATH}{MAP_LIST_PATH}', 'w+')
    if final_map_file is not None:
        map_string = string_builder(args, map_list, maps, final_map_file)
        final_map_file.write(map_string)
        print('New ', 'server file ' if not args.list and server_file_exists else 'map list ', 'generated! Find you new file here: ', args.ServerFile if not args.list and server_file_exists else f'{DIR}{MAP_LIST_DIR_PATH}{MAP_LIST_PATH}')
    else:
        raise Exception('final_map_file not opened. Contact dev for assistance here https://github.com/ScidaJ/MW2MapScramblerPython')

def string_builder(args, map_list: dict, master_map_list: dict, map_file: TextIOWrapper) -> str:
    file_slices = None
    maps = ''
    map_prefix = args.prefix if args.prefix is not None else ''

    if args.ArgSliceChar is not None and args.ServerFile is not None:
        file_slices = map_file.read().split(args.ArgsSliceChar)
        maps.join(file_slices[0])
    elif args.PreArg is not None:
        maps.join(args.PreArg)
        
    for idx, curr_map in enumerate(map_list):
        maps.join((map_prefix, master_map_list[map_list[curr_map]], ' ' if idx < len(map_list) - 1 else map_prefix, master_map_list[map_list[curr_map]]))

    if args.ArgSliceChar is not None and args.ServerFile is not None:
        maps.join(file_slices[2])
    elif args.PreArg is not None:
        maps.join(args.PostArg)

    return maps

def validate_args(args):
    valid = True

    if not exists(args.MapList):
        print('Your map file ', args.MapFile, ' does not exist. Exiting.')
        valid = False

    if args.ArgSliceChar is not None and args.ServerFile is None:
        print('ArgSliceChar specified but no ServerFile given. Ignoring ArgSliceChar. Please remove ArgSliceChar in the future.')
        input()

    if args.ArgSliceChar is not None and args.ServerFile is not None and (args.PreArg is not None or args.PostArg is not None):
        print('ArgSliceChar, ServerFile, PreArg or PostArg all defined. This is not allowed. Exiting.')
        valid = False

    if args.list and args.ServerFile is not None:
        print('--list set to true when ServerFile is provided. Do not use these together.')
        valid = False
    

    if not valid:
        input()
        exit()

if __name__ == '__main__':
    main()

