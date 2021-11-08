#!/usr/bin/python3-64 -X utf8


import argparse
from collections import defaultdict as dd
import hashlib
import os
import platform
import sys
import time


__author__ = 'Brandon Wells <wellsb.prog@gmail.com>'
__license__ = 'MIT'
__origin_date__ = '2021-11-06'
__prog__ = 'hash.py'
__purpose__ = 'Calculate hash codes for files'
__version__ = '1.0.0'
__version_date__ = '2021-11-07'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())
ver = f'{__prog__} v{__version__} ({__version_date__})'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hash_check(h: str):
    """This function executes the hashing algorithm. There is no return. The
       global variable is updated on each pass through this function.

    Args:
        h (str): the hash type to use

    Returns:
        hash_check_return (str): the hexidecimal hash value of the file
    """
    # hashlib function variable
    hf_var = (getattr(hashlib, h)())
    # use try when opening file to prevent crash from rights or other issues
    try:
        with open(args.file, 'rb') as f:
            # while loop to read file in chunks
            while True:
                f_chunk = f.read(args.blocksize * hf_var.block_size)
                if not f_chunk:
                    break
                hf_var.update(f_chunk)
    except OSError as e:
        # print the file open error and exit
        print(f'Error: unable to open {args.file}.\nError: {e}')
        sys.exit(1)

    if 'shake' in h:  # shake hashes require length variable
        hash_check_return = hf_var.hexdigest(args.length)
    else:  # all other hashes
        hash_check_return = hf_var.hexdigest()

    return hash_check_return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    # if verbose requested, print platform variables and arguments
    if args.verbose:
        print(f'Program: {ver}\nEnvirontment:\n\tPython: v'
              f'{platform.python_version()}\n\tInterpreter: '
              f'{platform.python_implementation()}\n\tCompiler: '
              f'{platform.python_compiler()}\nPlatform:\n\tOS: '
              f'{platform.platform()}\n\tCPU: {platform.processor()}\n'
              f'Variables:\n\tFile: {args.file}\n\tHash: {args.hash}\n\tLength'
              f': {args.length}\n\tBlocksize: {args.blocksize}\n')
    # create default dict of tuples to hold the hash return values
    hash_dict = dd(tuple)
    if args.all:  # check if all hashs are requested and loop through them
        for h_entry in sorted(hashlib.algorithms_guaranteed):
            # using time.monotonic to track the function start and stop time
            m_start = time.monotonic()
            # call the hash function and assign to hash_hex string
            hash_hex = hash_check(h_entry)
            m_stop = time.monotonic()
            # populate this default dict with every hash
            hash_dict[h_entry] += (m_stop - m_start, hash_hex)
    else:  # else generate a hash of the specified type
        # using time.monotonic to track the function start and stop time
        m_start = time.monotonic()
        # call the hash function and assign to hash_hex string
        hash_hex = hash_check(args.hash)
        m_stop = time.monotonic()
        # even though single, also assign to dict for single print command
        hash_dict[args.hash] += (m_stop - m_start, hash_hex)
    # print the hash or hashes
    print('Hash:\t    Time:\tHex Value:')
    for key, value in hash_dict.items():
        # :<12s = 12 spaces with string; :.4f = 4 place accuracy after decimal
        print(f'{key:<12s}{value[0]:.4f}s\t{value[1]}')


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
                        help='hash type to use',
                        metavar='<hash>',
                        type=str,
                        default='sha256')
    parser.add_argument('-l',
                        '--length',
                        help='"shake" hash requires a length value',
                        metavar='<number>',
                        type=int,
                        default=32)
    parser.add_argument('--all',
                        help='run all available hashes against file',
                        action='store_true')
    parser.add_argument('-a',
                        '--available',
                        help='print available hashes and their blocksizes',
                        action='store_true')
    parser.add_argument('-b',
                        '--blocksize',
                        help='specify file read blocksize multiplier (consumes'
                             ' more ram for faster processing)',
                        metavar='<number>',
                        type=int,
                        default=128)
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

    if args.available:  # print available hashes and exit if requested
        print(f'{ver}\nAvailable hashes:\nHash:\t\tBlock size:\tDigest Size:')
        for i in sorted(hashlib.algorithms_guaranteed):
            print(f'{i:<15s} {getattr(hashlib, i)().block_size:<16}'
                  f'{getattr(hashlib, i)().digest_size}')
        sys.exit(0)
    if args.file:  # check to confirm if the file exists
        if not os.path.isfile(args.file):
            print(f'Error: file "{args.file}" does not exist.')
            sys.exit(1)
    else:  # exit if the file does not exist
        print('Error: no file specified')
        sys.exit(1)
    # check to confirm the hash requested is supported
    if args.hash.lower() not in hashlib.algorithms_guaranteed:
        print(f'Error: hash "{args.hash}" invalid or unavailable.')
        sys.exit(1)
    # confirm the length and blocksize variables are greather than 0
    if args.length < 1:
        print(f'Error: {args.length} invalid. Length must be 1 or greater.')
        sys.exit(1)
    if args.blocksize < 1:
        print(f'Error: {args.blocksize} invalid. Length must be 1 or greater.')
        sys.exit(1)

    main()
