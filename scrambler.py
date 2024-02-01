import argparse
import random
from io import TextIOWrapper
from os import getcwd
from os.path import exists
from pathlib import Path
from sys import exit

DIR = getcwd()
OUT_DIR_PATH = '\out'
MAP_LIST_FILE = '\maps.txt'
SERVER_FILE_COPY = '\server_copy.cfg'

def main(): 
    
    args = prase_args()

    validate_args(args)

    maps = {}
    random_map_list = {}
    output_file = None
    server_file = None
    output_file_path = ''
    output_file_name = args.OutputFile if args.OutputFile is not None else SERVER_FILE_COPY
    map_string = ''
    map_file = Path(args.MapList).read_text().split('\n')
    server_file_exists = False

    map_filter = ingest_filter(args)

    #ingest_filter(args) will alter the final size of the map list, so it must be calculated after the filter is generated.
    size = (len(map_file) - 1) if map_filter == '' else ((len(map_file) - 1) - len(map_filter.split(',')))

    random_map_list_builder(map_filter, map_file, maps, random_map_list, size)
    
    print('Maps have been scrambled, writing to', 'list file' if args.ServerFile is None else 'server file')

    if args.ServerFile is not None:
        server_file_exists = exists(args.ServerFile)
    
    if args.ServerFile is not None and not server_file_exists:
        print('Your server file', args.ServerFile, 'does not exist. Check the file path.')
        input()
        exit()
    elif server_file_exists:
        if args.OutputDir is not None:
             output_file_path = f'{args.OutputDir}{output_file_name}'
        elif not args.override:
            output_file_path = f'{DIR}{OUT_DIR_PATH}{output_file_name}'
        else:
            output_file_path = args.ServerFile
        server_file = open(args.ServerFile, 'r+')
        output_file = open(output_file_path, 'w+') if not output_file_path is args.ServerFile else server_file
    else:
        print('Creating directory and map list file if it does not exist.')
        args.ServerFile = None
        Path(f'{DIR}{OUT_DIR_PATH}').mkdir(parents=True, exist_ok=True)
        output_file_path = f'{DIR}{OUT_DIR_PATH}{MAP_LIST_FILE}'
        output_file = open(output_file_path, 'w+')
    
    if output_file is not None:
        map_string = string_builder(args, random_map_list, maps, server_file)
        output_file.seek(0)
        output_file.write(map_string)
        output_file.truncate()
        print('New', 'server file' if server_file_exists else 'map list', 'generated! Find your new file here:', output_file_path, '\nThe first map is', random_map_list[0])
    else:
        raise Exception('final_map_file not opened. Contact dev for assistance here https://github.com/ScidaJ/MapScramblerPython')

def prase_args(argv):
    parser = argparse.ArgumentParser(prog='scrambler.py')
    parser.add_argument('MapList', help='Path to the map list that you want to use with the scrambler. Will not create if it does not exist.')
    parser.add_argument('--ServerFile', help='Path to the server startup file or the file which contains the map list. Will not create if it does not exist. Do not use with --list.')
    parser.add_argument('--PreArg', help='Arguments that go before the map list. Spaces/New lines will not be added to the end.')
    parser.add_argument('--PostArg', help='Arguments that go after the map list. Spaces/New lines will not be added to the front.')
    parser.add_argument('--ArgSliceChar', help='Character to slice the server arguments by. Must be exactly 2 slice characters in server file, One directly before the map list, and one directly after. CANNOT be used with --PreArg or --PostArg.')
    parser.add_argument('--OutputDir', help='The directory where you would like to output the final copy. Not to be used with -o.')
    parser.add_argument('--OutputFile', help='The name of the output file. Not to be used with -o.')
    parser.add_argument('--Filter', help='Provide a CSV list of maps or path to a file containing one to be filtered out of the scramble.', default='')
    parser.add_argument('-o', '--override', help='Overwrites original server.cfg with scrambled version. Only use this if you know what you are doing. Not to be used with -l.', action='store_true')
    parser.add_argument('-p', '--prefix', help='Prefix for map names. Space will not be added if they exist. E.g. mp [mapName]')
    parser.add_argument('-q', '--quotes', help='Encapsulates the map list in quotes.', action='store_true')
    parser.add_argument('-v', '--verbose', help='Enables verbose output.', action='store_true')

    return parser.parse_args(argv)

def random_map_list_builder(map_filter, map_file, maps, random_map_list, size):
    for curr_map in map_file:
        curr_map = curr_map.split(',')
        if curr_map[1] not in map_filter:
            maps[curr_map[1]] = curr_map[0]
            index = random.randint(0, size)
            while index in random_map_list:
                index = random.randint(0, size)
            random_map_list[index] = curr_map[1]

def ingest_filter(args):
    if len(args.Filter) != 0 and '.txt' in args.Filter[(len(args.Filter) - 4):]:
            map_filter = Path(args.Filter).read_text()
            return map_filter
    else:
        return args.Filter

def string_builder(args, random_map_list: dict, map_list: dict, server_file: TextIOWrapper) -> str:
    size = len(random_map_list) - 1
    file_slices = None
    maps = ''
    map_prefix = args.prefix if args.prefix is not None else ''

    if args.ArgSliceChar is not None and server_file is not None:
        file_slices = server_file.read().split(args.ArgSliceChar)
        maps += file_slices[0]
    elif args.PreArg is not None:
        maps += args.PreArg

    if args.quotes:
        maps += '\"'

    for i in range(size):
        next_map = map_prefix + map_list[random_map_list[i]] + (' '  if i < size - 1 else '')
        maps = ''.join((maps, next_map))

    if args.quotes:
        maps += '\"'

    if args.ArgSliceChar is not None and server_file is not None:
        maps += file_slices[2]
    elif args.PostArg is not None:
        maps += args.PostArg

    return maps

def validate_args(args):
    valid = True

    if not exists(args.MapList):
        print('Your map file {0} does not exist. Exiting.'.format(args.MapList))
        valid = False

    if args.override:
        print('--override is set. Exit program with Ctrl + C if this is not correct, otherwise hit Enter.')
        input()

    if args.override and args.ServerFile is None:
        print('--override provided with no --ServerFile, this is not allowed. Exiting.')
        valid = False

    if args.ArgSliceChar is not None and args.ServerFile is None:
        print('ArgSliceChar specified but no ServerFile given. Ignoring ArgSliceChar. Please remove ArgSliceChar in the future.')
        input()

    if args.ArgSliceChar is not None and args.ServerFile is not None and (args.PreArg is not None or args.PostArg is not None):
        print('ArgSliceChar, ServerFile, PreArg or PostArg all defined. This is not allowed. Exiting.')
        valid = False

    if args.OutputDir is not None and args.override:
        print('--OutputDir cannot be used with -o. Exiting.')
        valid = False

    if args.OutputFile is not None and args.override:
        print('--OutputFile cannot be used with -o. Exiting.')
        valid = False

    if args.Three and len(args.MapTypes) == 4:
        print('You have selected all map types. This would result in an empty map list. Please remove at least one map type from your filter. Exiting.')
        valid = False
    
    if '.txt' in args.Filter[(len(args.Filter) - 4):] and not exists(args.Filter):
        print('The filter file you provided does not exist. Exiting.')
        valid = False

    if not valid:
        print('Press Enter to exit.')
        input()
        exit()

if __name__ == '__main__':
    main()
