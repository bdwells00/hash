#!/usr/bin/python3-64 -X utf8


import argparse
from collections import defaultdict
from datetime import datetime
import hashlib
from math import ceil
import os
import platform
import sys
import time
# constant 1k multiplier for args.blocksize
BLOCK_SIZE_FACTOR = 1000
START_PROG_TIME = time.monotonic()


__author__ = 'Brandon Wells <wellsb.prog@gmail.com>'
__license__ = 'MIT'
__origin_date__ = '2021-11-06'
__prog__ = 'hash.py'
__purpose__ = 'Calculate hash codes for files.'
__version__ = '1.4.6'
__version_date__ = '2021-12-01'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())
ver = f'{__prog__} v{__version__} ({__version_date__})'
# global print tracker only updated via bp
print_tracker = 0                                               # from bp 0.1.2
# create list of available hash algorithms
hash_list = [i for i in sorted(hashlib.algorithms_guaranteed)]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Ct:                                                       # from bp 0.1.2
    """A class of constants used to color strings for console printing. Using
    the full Unicode escape sequence to allow both 8 and 24 bit color here."""
    # ~~~ #     3-bit/4-bit in 8 bit (256) unicode, plus some grey 256
    A = '\u001b[0m'                         # reset (all attributes off)
    RED = '\u001b[38;5;1m'                  # red
    GREEN = '\u001b[38;5;2m'                # green
    YELLOW = '\u001b[38;5;3m'               # yellow
    BBLUE = '\u001b[38;5;12m'               # bright blue
    BMAGENTA = '\u001b[38;5;13m'            # bright magenta
    GREY1 = '\u001b[38;5;255m'              # grey level 1
    # ~~~ #     some 24-bit unicode colors
    ORANGE = '\u001b[38;2;233;133;33m'      # orange


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_args():
    """Get CLI arguments from argparse.

    Returns:
        - class 'argparse.ArgumentParser': Command Line Arguments
    """
    # Use argparse to capture cli parameters
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=f'{Ct.BBLUE}{ver}: {__purpose__}{Ct.A}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f'{Ct.RED}This program has no warranty. Please use with caution'
               f'.{Ct.A}',
        add_help=True)
    parser.add_argument('-f',
                        '--file',
                        help='file to generate hash against',
                        metavar=f'{Ct.RED}<filename>{Ct.A}',
                        type=str)
    parser.add_argument('--hash',
                        help='hash type to use; ignored if all is used',
                        metavar=f'{Ct.YELLOW}<hash>{Ct.A}',
                        type=str,
                        default='sha256')
    parser.add_argument('-l',
                        '--length',
                        help='"shake" hash requires a digest length value (1-'
                             '128); ignored for all other hashes',
                        metavar=f'{Ct.YELLOW}<number>{Ct.A}',
                        type=int,
                        default=32)
    parser.add_argument('--all',
                        help='run all available hashes against file; cannot '
                             'be used with --compare',
                        action='store_true')
    parser.add_argument('--available',
                        help='print available hashes, their values, and exit',
                        action='store_true')
    parser.add_argument('-b',
                        '--blocksize',
                        help='specify number of 1kB read blocks (1-100000000);'
                             'consumes more ram for minimally faster'
                             ' processing',
                        metavar=f'{Ct.YELLOW}<number>{Ct.A}',
                        type=int,
                        default=16)
    parser.add_argument('-c',
                        '--compare',
                        help='value to compare against generated hash; cannot '
                             'be used with --all',
                        metavar=f'{Ct.YELLOW}<value>{Ct.A}',
                        type=str)
    parser.add_argument('--no-color',
                        help='don\'t colorize output',
                        action='store_true')
    parser.add_argument('-v',
                        '--verbose',
                        help='3 lvl incremental verbosity (-v, -vv, or -vvv)',
                        action='count',
                        default=0)
    parser.add_argument('--version',
                        help='print program version and exit',
                        action='version',
                        version=f'{Ct.BBLUE}{ver}{Ct.A}')

    return parser.parse_args()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def validate_and_process_args(h_list: list):
    """Validate and process the cli args before executing main()."""
    bp([f'entered validate_and_process_args({h_list})', Ct.BMAGENTA], veb=3)
    bp(['confirm the length and blocksize variables are within set limits',
        Ct.BMAGENTA], veb=3)
    if args.length < 1 or args.length > 128:
        bp([f'"--length {args.length}" invalid. Length must be between (and '
            'including) 1 and 128.', Ct.RED], erl=2)
        sys.exit(1)
    if args.blocksize < 1 or args.blocksize > 100000000:
        bp([f'"--blocksize {args.blocksize}" invalid. Length must between (and'
            ' including) 1 and 100000000.', Ct.RED], erl=2)
        sys.exit(1)
    bp(['print available hashes and exit if requested', Ct.BMAGENTA], veb=3)
    if args.available:
        bp(['Available:\nHash:\t\tBlock size:\tDigest Length:\tHex Length:',
            Ct.A])
        for i in h_list:
            if 'shake' not in i:
                bp([f'{i:<16s}', Ct.RED,
                    f'{getattr(hashlib, i)().block_size:<16}'
                    f'{getattr(hashlib, i)().digest_size:<16}'
                    f'{2 * getattr(hashlib, i)().digest_size:<16}', Ct.BBLUE],
                    num=0)
            else:
                bp([f'{i:<16s}', Ct.RED,
                    f'{getattr(hashlib, i)().block_size:<16}{args.length:<16}'
                    f'{2 * args.length:<16}', Ct.BBLUE], num=0)
        sys.exit(0)
    bp([f'check to confirm {args.file} exists.', Ct.BMAGENTA], veb=3)
    if args.file:
        if not os.path.isfile(args.file):
            bp([f'"--file {args.file}" does not exist.', Ct.RED], erl=2)
            sys.exit(1)
    else:
        bp(['no file specified.', Ct.RED], erl=2)
        sys.exit(1)
    bp(['if not processing all hash, reset h_list to just the one hash',
        Ct.BMAGENTA], veb=3)
    if not args.all:
        bp([f'check to confirm the hash requested, {args.hash.lower()} is'
            ' supported.', Ct.BMAGENTA], veb=3)
        if args.hash.lower() not in h_list:
            bp([f'"--hash {args.hash}" invalid or unavailable.', Ct.RED],
               erl=2)
            sys.exit(1)
        else:
            h_list = [args.hash.lower()]
    bp(['--compare and --all are mutually exclusive; exit if both requested.',
        Ct.BMAGENTA], veb=3)
    if args.compare and args.all:
        bp(['cannot combine "--compare" with "--all".', Ct.RED], erl=2)
        sys.exit(1)
    bp([f'returning {h_list}.', Ct.BMAGENTA], veb=2, num=0)
    return h_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bp(txt: list, erl=0, fil=1, fls=0, inl=0, log=1, num=1, veb=0):  # bp 0.1.2
    """Better Print: send output commands here instead of using print command.
    Txt must be sent in the form of pairs of strings in a list. The even
    strings ("0", "2", "4", etc.) contain the output text while the odd strings
    ("1", "3", "5", etc.) contain the color companion that defines the color
    to be applied to the preceding string. There are pre-defined defaults that
    can be overwritten but not required.

    Example:
        - bp(['Hello', Ct.RED, 'world', Ct.A, '!', Ct.GREEN], veb=2)
            - This prints "Hello world!" with the Hello in red, world in
            terminal default color, and the bang in green. This will also only
            print if args.verbose is set to "2" via "-vv".

    Args:
        - txt (list): (required) must be pairs with the even entries a string
                      and odd sections the Ct.color to apply to that string.
        - erl  (int): (optional) 0 = none (default), 1 = WARNING, 2 = ERROR:
                      auto pre-pends ERROR: or WARNING:, colors line Red, and
                      allows routing of only these to error log if requested.
        - fil  (int): (optional) 0 = off, 1 (default)= on: setting zero skips
                      file output even if args requested.
        - fls  (int): (optional) 0 = off (default), 1 = on: flush the text
                      instead of holding on to it. Usually required for in-
                      line text (inl=1) to force output without an end-of-line.
        - inl  (int): (optional) 0 = off (default); 1 = on: text written in-
                      line with no end-of-line character. Make sure to invoke
                      eol with a final bp before moving on.
        - log  (int): (optional) 0 = off; 1 = on (default): allow pre-pend of
                      each print statement with the date. Can be turned off for
                      things like progress bars and % updates.
        - num  (int): (optional) 0 = off; 1 = on (default): print blue numbers
        - veb  (int): (optional) 0-3: value is used to print only as much as
                      requested.

    Return:
        - None
    """
    # ~~~ #     variables section
    # this keeps track of the number of non-inline print statements
    global print_tracker
    # local variables - txt_tmp gets colored, file_tmp does not
    txt_out, file_out = '', ''
    # this provides an empty dict of args in case no args
    args_dict = vars(args) if 'args' in globals() else {}

    # ~~~ #     validate verbosity
    # if verbose not implemented, print everything
    if 'verbose' in args_dict:
        # if error logging set, veb ignored and will be printed
        if args.verbose < veb and erl == 0:
            return      # skip anything with higher verbosity than requested

    # ~~~ #     validate txt list - verify it is in pairs
    txt_l = len(txt)
    if txt_l % 2 != 0:
        raise Exception(f'{Ct.RED}"Better Print" function (bp) -> "txt: (list)'
                        f'": must be in pairs (txt length = {txt_l}){Ct.A}')

    # ~~~ #     veb section - prepend INFO-L(x) to each output with verbose
    if veb > 0 and erl == 0 and log == 1:
        txt_out = f'INFO-L{veb}: '
        file_out = f'INFO-L{veb}: '

    # ~~~ #     error section - pre-pend Error or Warning
    # this overwrites veb section as errors and warnings take precedence
    if erl == 1:
        txt_out = f'{Ct.YELLOW}WARNING: {Ct.A}'
        file_out = 'WARNING: '
    elif erl == 2:
        txt_out = f'{Ct.RED}ERROR: {Ct.A}'
        file_out = 'ERROR: '

    # ~~~ #     colorize and assemble section
    # need enumerate to identify even entries that contain strings
    for idx, val in enumerate(txt):
        if idx % 2 == 0:
            if type(val) != str:
                raise Exception(f'{Ct.RED}"Better Print" function (bp) -> "txt'
                                f' list even entries must be str. txt type = '
                                f'{type(val)}{Ct.A}')
            ent = ''
            j = txt[idx + 1]
            # colorize numbers and reset to default
            if num == 1 and j == Ct.A:
                for i in val[:]:
                    ent += f'{Ct.BBLUE}{i}{Ct.A}' if i.isdigit() else i
            # colorize numbers and reset to requested color for that part
            elif num == 1:
                for i in val[:]:
                    ent += f'{Ct.BBLUE}{i}{j}' if i.isdigit() else i
            # don't colorize numbers
            else:
                ent = val
            # now wrap the color numbered string with the requested color
            txt_out += f'{j}{ent}{Ct.A}'
            # file output is the original value with no console coloration
            file_out += val[:]

    # ~~~ #     log section - prepend time to each output
    # skip if log is not implemented in args
    if 'log' in args_dict:
        if args.log and log == 1:
            dt_now = datetime.now().strftime('[%H:%M:%S]')
            txt_out = f'{dt_now}-{print_tracker}-{txt_out}'
            file_out = f'{dt_now}-{print_tracker}-{file_out}'

    # ~~~ #     no color check
    # skip if no_color not implemented in args
    if 'no_color' in args_dict:
        if args.no_color:
            txt_out = file_out[:]

    # ~~~ #     console output section
    if inl == 0:    # default with new line appended
        sys.stdout.write(f'{txt_out}\n')
        print_tracker += 1
    elif inl == 1 and fls == 0:     # in-line with no flush
        sys.stdout.write(txt_out)
    elif inl == 1 and fls == 1:     # in-line with flush
        sys.stdout.write(txt_out)
        sys.stdout.flush()

    # ~~~ #     file output section
    # skip if file log output not implemented in args
    if 'log_file' in args_dict or 'error_log_file' in args_dict:
        try:
            if args.log_file and fil == 1:
                with open(args.log_file, 'a') as f:
                    f.write(file_out + '\n')
            if args.error_log_file and erl > 0 and fil == 1:
                with open(args.error_log_file, 'a') as f:
                    f.write(file_out + '\n')
        except OSError as e:
            bp([f'exception caught trying to write to {args.log_file} or '
                f'{args.error_log_file}\n\t{e}', Ct.RED], erl=1, fil=0)

    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hash_check(h: str):
    """This function reads the file in chunks and executes the hashing
       algorithm. This tracks the file read times along with the hashing time.

    Args:
        - h (str): this is the type of hash to execute on this function

    Returns:
        - tuple: the time to read the file, the time to hash the file, and the
               standard hexadecimal hash output of the requested type.
    """
    bp([f'entering hash_check({h}).', Ct.BMAGENTA], veb=3, num=0)
    bp(['create hf_var function variable using the hash.', Ct.BMAGENTA], veb=3)
    hf_var = (getattr(hashlib, h)())
    bp(['create file & hash time vars, and hex var', Ct.BMAGENTA], veb=3)
    file_time, hash_time, hash_hex = 0, 0, ''

    # ~~~ #     read & hash section
    bp(['open file with "try:".', Ct.BMAGENTA], veb=3)
    try:
        f_info = os.stat(args.file, follow_symlinks=False)
        file_loop = 0
        f_loops = ceil(f_info.st_size / (args.blocksize * BLOCK_SIZE_FACTOR))
        update_loop = 1 if f_loops < 100 else int(f_loops / 100)
        with open(args.file, 'rb') as f:
            bp(['while loop to read file in chunks and hash each chunk.',
                Ct.BMAGENTA], veb=3)
            # uncomment the bp sections under while loop only for testing
            # on small files. Performace is crushed on large files with
            # many loops.
            while True:
                # bp(['start the file read time tracking.', Ct.BMAGENTA],
                    #  veb=3)       # noqa
                f_start = time.monotonic()
                # bp(['read a block of the file (default 16k).', Ct.BMAGENTA],
                    # veb=3)       # noqa
                f_chunk = f.read(args.blocksize * BLOCK_SIZE_FACTOR)
                # bp(['stop the file read time tracking', Ct.BMAGENTA], veb=3)
                f_stop = time.monotonic()
                # bp(['add/append file reading to the time variable,
                    #  file_time.', Ct.BMAGENTA], veb=3)       # noqa
                file_time += (f_stop - f_start)
                # bp(['break the while loop when the file chunk is empty',
                    # Ct.BMAGENTA], veb=3)       # noqa
                if not f_chunk:
                    break
                # bp(['start the hash time tracking.', Ct.BMAGENTA], veb=3)
                h_start = time.monotonic()
                # bp(['hash the file chunk.', Ct.BMAGENTA], veb=3)
                hf_var.update(f_chunk)
                # bp(['stop the hash time tracking.', Ct.BMAGENTA], veb=3)
                h_stop = time.monotonic()
                # bp(['add/append hashing to the hash time variable,
                    # hash_time', Ct.BMAGENTA], veb=3)       # noqa
                hash_time += (h_stop - h_start)
                file_loop += 1
                if file_loop % update_loop == 0:
                    bp([f'\u001b[1000D{(file_loop / f_loops) * 100:.0f}',
                        Ct.BBLUE, '% | Hash: ', Ct.A, f'{h:<9s}', Ct.RED,
                        ' | ', Ct.A, 'File: ', Ct.A, f'{args.file}', Ct.GREEN],
                        inl=1, num=0, fls=1)
            bp(['', Ct.A])
    except OSError as e:
        bp([f'unable to open {args.file}.\n\t{e}', Ct.RED], erl=2)
        sys.exit(1)

    # ~~~ #     conversion and processing section
    bp(['start the hash time tracking for conversion to hex.', Ct.BMAGENTA],
        veb=3)
    h_start = time.monotonic()
    bp(['hex convert (provide shake the requested length).', Ct.BMAGENTA],
        veb=3)
    if 'shake' in h:
        hash_hex = hf_var.hexdigest(args.length)
    else:
        hash_hex = hf_var.hexdigest()
    bp(['stop the hash time tracking for conversion to hex.', Ct.BMAGENTA],
        veb=3)
    h_stop = time.monotonic()
    bp(['add/append hashing to the hash time variable, hash_time',
        Ct.BMAGENTA], veb=3)
    hash_time += (h_stop - h_start)
    bp([f'returning tuple of ({file_time}, {hash_time}, {hash_hex})',
        Ct.BMAGENTA], veb=3, num=0)

    return file_time, hash_time, hash_hex


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main(h_list: list):

    bp([f'entered main({h_list}).', Ct.BMAGENTA], veb=3, num=0)
    bp([f'Python: v{platform.python_version()}', Ct.BBLUE, ' | ', Ct.A,
        f'{platform.python_implementation()}', Ct.BBLUE, ' | ', Ct.A,
        f'{platform.python_compiler()}', Ct.BBLUE], veb=1, log=0)
    bp([f'OS: {platform.platform()}', Ct.GREEN, ' | ', Ct.A,
        f'{platform.processor()}', Ct.GREEN], veb=1, log=0)
    bp(['Args: ', Ct.A], inl=1, veb=1, log=0)
    for k, v in vars(args).items():
        if k == 'hash':
            bp([f' {k}', Ct.GREEN, ':', Ct.A, f'{v}', Ct.RED, ' |', Ct.A],
                num=0, inl=1, veb=1, log=0)
        elif k == 'compare':
            bp([f' {k}', Ct.GREEN, f': {v} |', Ct.A], num=0, inl=1, veb=1,
                log=0)
        else:
            bp([f' {k}', Ct.GREEN, f': {v} |', Ct.A], inl=1, veb=1, log=0)
    bp(['\u001b[1D \n', Ct.A], veb=1, log=0, num=0)
    bp(['create a default dict, "hash_output" of type tuple, to hold the '
        'output. Each hash gets its own entry. create "cumulative_time" to '
        'hold duration of all file and hash times.', Ct.BMAGENTA], veb=3)
    hash_output, cumulative_time = defaultdict(tuple), 0
    bp(['cycle through each entry in "h_list" assigning hash_output.',
        Ct.BMAGENTA], veb=2, num=0)
    for hash_type in h_list:
        bp([f'calling hash_check({hash_type})', Ct.BMAGENTA], veb=3, num=0)
        hash_output[hash_type] = hash_check(hash_type)
    bp(['\nHash:\t    File Time:\tHash Time:\tHex Value:', Ct.A])
    for k, v in hash_output.items():
        bp([f'{k:<12s}', Ct.RED, f'{v[0]:.4f}s\t{v[1]:.4f}s\t\t', Ct.BBLUE,
            f'{v[2]}', Ct.A], num=0)
        cumulative_time += v[0]
        cumulative_time += v[1]
    bp(['print hash comparisons if requested.', Ct.BMAGENTA], veb=3)
    if args.compare:
        bp([f'\nGenerated: {hash_output[h_list[0]][2]}', Ct.A], num=0)
        if hash_output[h_list[0]][2] == args.compare:
            bp([f'Compared:  {args.compare}\n', Ct.A, 'HASHES MATCH!!',
                Ct.GREEN], num=0)
        else:
            bp([f'Compared:  {args.compare}\n', Ct.A, 'HASHES DO NOT MATCH!!',
                Ct.RED], num=0)
    bp(['generate program end time and calculate program overhead',
        Ct.BMAGENTA], veb=3)
    end_time = time.monotonic()
    total_time = end_time - START_PROG_TIME
    bp(['', Ct.A], log=0, veb=1)
    bp([f'program total time:    {total_time}s', Ct.BMAGENTA], veb=1, log=0)
    bp([f'program overhead time: {total_time - cumulative_time}s',
        Ct.BMAGENTA], veb=1, log=0)

    bp(['main() complete.', Ct.BMAGENTA], veb=3)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    # make args global
    args = get_args()
    bp([f'{ver}: {__purpose__}\n', Ct.BBLUE])
    bp([f'calling validate_and_process_args({hash_list}) and assigning back to'
        ' hash_list. Allows for all or just one hash.', Ct.BMAGENTA], veb=2,
        num=0)
    hash_list = validate_and_process_args(hash_list)
    bp([f'calling main({hash_list}).', Ct.BMAGENTA], veb=2, num=0)
    main(hash_list)
