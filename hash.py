#!/usr/bin/python3-64 -X utf8


import argparse
from collections import defaultdict
import hashlib
import os
import platform
import sys
import time
# constant 1k multiplier for args.blocksize
BLOCK_SIZE_FACTOR = 1024


__author__ = 'Brandon Wells <wellsb.prog@gmail.com>'
__license__ = 'MIT'
__origin_date__ = '2021-11-06'
__prog__ = 'hash.py'
__purpose__ = 'Calculate hash codes for files'
__version__ = '1.2.0'
__version_date__ = '2021-11-14'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())
ver = f'{__prog__} v{__version__} ({__version_date__})'
# create list of available hash algorithms
h_list = [i for i in sorted(hashlib.algorithms_guaranteed)]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hash_check(h: str):
    """This function reads the file in chunks, and executes the hashing
       algorithm. This tracks the file read times along with the hashing time.

    Args:
        h (str): this is the type of hash to execute on this function

    Returns:
        tuple: the time to read the file, the time to hash the file, and the
               standard hash output of the requested type for the file.
    """
    # hashlib function variable
    hf_var = (getattr(hashlib, h)())
    # create file & hash time vars, and hex var
    file_time, hash_time, hash_hex = 0, 0, ''
    # use try when opening file to prevent crash from rights or other issues
    try:
        with open(args.file, 'rb') as f:
            # while loop to read file in chunks and hash each chunk
            while True:
                # start the file read time tracking
                f_start = time.monotonic()
                # read a block of the file (default 8k)
                f_chunk = f.read(args.blocksize * BLOCK_SIZE_FACTOR)
                # stop the file read time tracking
                f_stop = time.monotonic()
                # add/append file reading to the time var
                file_time += (f_stop - f_start)
                # the while loop break for when the file read completes
                if not f_chunk:
                    break
                # start the hash time tracking
                h_start = time.monotonic()
                # update the specific hash chunk
                hf_var.update(f_chunk)
                # stop the hash time tracking
                h_stop = time.monotonic()
                # add/append hashing to the time var
                hash_time += (h_stop - h_start)
    except OSError as e:
        # print the file open error and exit
        print(f'Error: unable to open {args.file}.\nError: {e}')
        sys.exit(1)

    # convert to standard hexadecimal output
    # start the hash time tracking
    h_start = time.monotonic()
    if 'shake' in h:  # shake hashes require length variable
        hash_hex = hf_var.hexdigest(args.length)
    else:  # all other hashes
        hash_hex = hf_var.hexdigest()
    # stop the hash time tracking
    h_stop = time.monotonic()
    # add/append hashing to the time var
    hash_time += (h_stop - h_start)

    return file_time, hash_time, hash_hex


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    # if verbose requested, print platform variables and arguments
    if args.verbose:
        h_str = ', '.join(h_list)
        print(f'Program: {ver}\nEnvironment:\n\tPython: v'
              f'{platform.python_version()}\n\tInterpreter: '
              f'{platform.python_implementation()}\n\tCompiler: '
              f'{platform.python_compiler()}\nPlatform:\n\tOS: '
              f'{platform.platform()}\n\tCPU: {platform.processor()}\n'
              f'Variables:\n\tFile: {args.file}\n\tHash: {h_str}\n\tLength'
              f': {args.length}\n\tBlocksize: {args.blocksize}kb '
              f'({args.blocksize} * {BLOCK_SIZE_FACTOR})\n')

    # create a default dict to hold the output
    hash_hex = defaultdict(tuple)
    # call the hash function and assign to hash_hex dict
    for hash_type in h_list:
        hash_hex[hash_type] = hash_check(hash_type)

    # print the hash or hashes
    print('Hash:\t    File Time:\tHash Time:\tHex Value:')
    for key, value in hash_hex.items():
        # :<12s = 12 spaces with string; :.4f = 4 place accuracy after decimal
        print(f'{key:<12s}{value[0]:.4f}s\t{value[1]:.4f}s\t\t{value[2]}')
    # print hash comparisons if requested
    if args.compare and not args.all:
        if hash_hex[h_list[0]][2] == args.compare:
            print(f'Generated: {hash_hex[h_list[0]][2]}\nCompared:  '
                  f'{args.compare}\nHashes match.')
        else:
            print(f'Generated: {hash_hex[h_list[0]][2]}\nCompared:  '
                  f'{args.compare}\nHASHES DO NOT MATCH!!')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    # Use argparse to capture cli parameters
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=f'{ver}: {__purpose__}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='This program has no warranty. Please use with caution. ',
        add_help=True
    )
    parser.add_argument('-f',
                        '--file',
                        help='file to generate hash against',
                        metavar='<filename>',
                        type=str)
    parser.add_argument('--hash',
                        help='hash type to use; ignored if all is used',
                        metavar='<hash>',
                        type=str,
                        default='sha256')
    parser.add_argument('-l',
                        '--length',
                        help='"shake" hash requires a digest length value; '
                             'ignored for all other hashes',
                        metavar='<number>',
                        type=int,
                        default=32)
    parser.add_argument('--all',
                        help='run all available hashes against file',
                        action='store_true')
    parser.add_argument('-a',
                        '--available',
                        help='print available hashes, their values, and exit',
                        action='store_true')
    parser.add_argument('-b',
                        '--blocksize',
                        help='specify number of 1K read blocks (consumes'
                             ' more ram for minimally faster processing)',
                        metavar='<number>',
                        type=int,
                        default=16)
    parser.add_argument('-c',
                        '--compare',
                        help='value to compare against generated hash; ignored'
                             ' if --all is used',
                        metavar='<value>',
                        type=str)
    parser.add_argument('-v',
                        '--verbose',
                        help='provide additional details',
                        action='store_true')
    parser.add_argument('--version',
                        help='print program version and exit',
                        action='version',
                        version=f'{ver}')

    # define args to process and make it globally available
    args = parser.parse_args()

    # confirm the length and blocksize variables are greather than 0
    if args.length < 1:
        print(f'Error: {args.length} invalid. Length must be 1 or greater.')
        sys.exit(1)
    if args.blocksize < 1:
        print(f'Error: {args.blocksize} invalid. Length must be 1 or greater.')
        sys.exit(1)
    # print available hashes and exit if requested
    if args.available:
        print(f'{ver}\nAvailable hashes:\nHash:\t\tBlock size:'
              '\tDigest Length:')
        for i in h_list:
            if 'shake' not in i:
                print(f'{i:<15s} {getattr(hashlib, i)().block_size:<16}'
                      f'{getattr(hashlib, i)().digest_size}')
            else:
                print(f'{i:<15s} {getattr(hashlib, i)().block_size:<16}'
                      f'{args.length}')
        sys.exit(0)
    if args.file:  # check to confirm if the file exists
        if not os.path.isfile(args.file):
            print(f'Error: file "{args.file}" does not exist.')
            sys.exit(1)
    else:  # exit if the file does not exist
        print('Error: no file specified')
        sys.exit(1)
    # if not processing all hash, reset h_list to just the one hash
    if not args.all:
        # check to confirm the hash request is supported
        if args.hash.lower() not in h_list:
            print(f'Error: hash "{args.hash}" invalid or unavailable.')
            sys.exit(1)
        else:
            h_list = [args.hash.lower()]

    main()
