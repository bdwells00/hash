#!/usr/bin/env python3

__author__ = 'Brandon Wells <wellsb.prog@gmail.com>'
__license__ = 'MIT'
__origin_date__ = '2021-11-06'
__prog__ = 'hash.py'
__purpose__ = 'Calculate hash codes for files.'
__version__ = '2.0.2'
__version_date__ = '2021-12-25'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())


import argparse
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
import hashlib
from math import ceil
import os
import platform
import sys
from time import perf_counter
# constant 1k multiplier for args.blocksize
BLOCK_SIZE_FACTOR = 1000
START_PROG_TIME = perf_counter()


# ~~~ #                 -global variables-
# global dict used to control bp functionality          # from betterprint 0.3.2
bp_dict = {
    'bp_tracker_all': 0,        # tracks all bp function calls
    'bp_tracker_con': 0,        # tracks only bp cli calls
    'bp_tracker_log': 0,        # tracks only bp log_file calls
    'bp_tracker_elog': 0,       # tracks only bp elog_file calls
    'color': 1,                 # override cli color
    'date_log': 0,              # prepend date to each output
    'log_file': None,           # the log file name for all output
    'error_log_file': None,     # the error log file name for only errors
    'quiet': 0,                 # allows surpressing cli errors
    'verbose': 0,               # match this verbose to bp veb; skip if lower
}
ver = f'{__prog__} v{__version__} ({__version_date__})'
hash_list = sorted(hashlib.algorithms_guaranteed)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@dataclass
class ColorText:                                        # from betterprint 0.3.2
    """A class of constants used to color strings for console printing.
    """
    __slots__ = (
        'a',
        'red',
        'green',
        'yellow',
        'bblue',
        'bmagenta',
        'grey1',
        'orange',
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def bp(txt: list, con=1, err=0, fil=1, fls=0, inl=0, log=1, num=1, veb=0):
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
        - con  (int): (optional) 0 = no console output, 1 = console output.
                      (default)
        - err  (int): (optional) 0 = none (default), 1 = WARNING, 2 = ERROR:
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
    # ~~~ #             -variables-
    global bp_dict
    bp_local_dict = {
        'con_out': '',
        'file_out': '',
    }

    # ~~~ #             -all print tracking-
    # track function call even if no output
    bp_dict['bp_tracker_all'] += 1

    # ~~~ #             -validate verbosity-
    if (err == 0 or bp_dict['quiet'] == 1) and bp_dict['verbose'] < veb:
        return      # skip higher veb as long as no errors or in quiet mode

    # ~~~ #             -validate txt list-
    # ensure each string has a color compliment within the list
    if len(txt) % 2 != 0:
        raise Exception(
            f'{Ct.red}"Better Print" (bp) function -> "txt: (list): '
            f'"must be in pairs (txt length = {len(txt)}){Ct.a}',
        )

    # ~~~ #             -veb-
    # prepend INFO-L(x) to output
    if veb > 0 and err == 0 and log > 0:
        bp_local_dict['con_out'] = f'INFO-L{veb}: '
        bp_local_dict['file_out'] = f'INFO-L{veb}: '

    # ~~~ #             -err-
    # pre-pend Error or Warning, overwriting -veb- section
    if err == 1:
        bp_local_dict['con_out'] = f'{Ct.yellow}WARNING: {Ct.a}'
        bp_local_dict['file_out'] = 'WARNING: '
    elif err == 2:
        bp_local_dict['con_out'] = f'{Ct.red}ERROR: {Ct.a}'
        bp_local_dict['file_out'] = 'ERROR: '

    # ~~~ #             -colorize and assemble-
    # need enumerate to identify even entries that contain strings
    for idx, val in enumerate(txt):
        if idx % 2 == 0:
            if not isinstance(val, str):
                raise Exception(
                    f'{Ct.red}"Better Print" (bp) function -> "txt list even '
                    f'entries must be str. txt type = {type(val)}{Ct.a}',
                )
            ttxt = ''               # even text val to be joined
            ctxt = txt[idx + 1]     # odd color val to color ttxt
            # colorize numbers and reset to default
            if num == 1 and ctxt == Ct.a:
                for idx in val[:]:
                    ttxt += f'{Ct.bblue}{idx}{Ct.a}' if idx.isdigit() else idx
            # colorize numbers and reset to requested color for that part
            elif num == 1:
                for idx in val[:]:
                    ttxt += f'{Ct.bblue}{idx}{ctxt}' if idx.isdigit() else idx
            # don't colorize numbers (equivalent to num=0)
            else:
                ttxt = val
            # now wrap the color numbered string with the requested color
            bp_local_dict['con_out'] += f'{ctxt}{ttxt}{Ct.a}'
            # file output is the original value with no console coloration
            bp_local_dict['file_out'] += val[:]

    # ~~~ #             -log-
    # allow log=0 to bypass this
    if bp_dict['date_log'] == 1 and log == 1:
        dt_now = datetime.now().strftime('[%H:%M:%S]')
        bp_local_dict['con_out'] = (
            f'{dt_now}-{bp_dict["bp_tracker_con"] + 1}-{bp_local_dict["con_out"]}'
        )
        bp_local_dict['file_out'] = (
            f'{dt_now}-{bp_dict["bp_tracker_log"] + 1}-{bp_local_dict["file_out"]}'
        )

    # ~~~ #             -color-
    # after all colorization sections, set cli to file if no color desired
    if bp_dict['color'] == 0:
        bp_local_dict['con_out'] = bp_local_dict['file_out'][:]

    # ~~~ #             -con-
    # skips con output if con=0
    if inl == 0 and con == 1:                   # default with new line
        sys.stdout.write(f'{bp_local_dict["con_out"]}\n')
        bp_dict['bp_tracker_con'] += 1
    elif inl == 1 and fls == 0 and con == 1:    # in-line with no flush
        sys.stdout.write(bp_local_dict['con_out'])
        bp_dict['bp_tracker_con'] += 1
    elif inl == 1 and fls == 1 and con == 1:    # in-line with flush
        bp_dict['bp_tracker_con'] += 1
        sys.stdout.write(bp_local_dict['con_out'])
        sys.stdout.flush()

    # ~~~ #             -file-
    try:
        # skip if file loging not requested or fil=0
        if bp_dict['log_file'] and fil == 1:
            with open(bp_dict['log_file'], 'a') as f:
                f.write(bp_local_dict['file_out'] + '\n')
        # separate errors into dedicated error log
        if bp_dict['error_log_file'] and err > 0 and fil == 1:
            with open(bp_dict['error_log_file'], 'a') as f:
                f.write(bp_local_dict['file_out'] + '\n')
    except OSError as e:
        bp([f'exception caught trying to write to {bp_dict["log_file"]} '
            f'or {bp_dict["error_log_file"]}\n\t{e}', Ct.red], err=1, fil=0)

    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def perf_timer(func):
    """The decorator time function. This is the encapsulating timer
        functionthat takes one argument, the child function, to calculate the
        duration of time.

    - Args:
        - child_function ([function]): the child function to execute

    - Return:
        - wrapper_function: tuple
            - 0: child function name
            - 1: duration the time function ran using time.monotonic
            - 2: the child function return
    """
    # ~~~ #             -timer-
    # using functools.wraps to pass along the child_function details
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        """The decorator time function. This is the timer function
         that takes one argument, the child function, to calculate the
         duration of time.

        - Args:
            - child_function ([function]): the child function to execute

        - Return:
            - wrapper_function: tuple
                - 0: child function name
                - 1: duration the time function ran using time.perf_counter
                - 2: the child function return
        """
        t_start = perf_counter()
        return_var = func(*args, **kwargs)
        t_stop = perf_counter()
        return func.__name__, t_stop - t_start, return_var
    return wrapper_function


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_args():
    """Get CLI arguments from argparse.

    Returns:
        - class 'argparse.ArgumentParser': Command Line Arguments
    """
    # ~~~ #                 -args-
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=f'{Ct.bblue}{ver}: {__purpose__}{Ct.a}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f'{Ct.red}This program has no warranty. Please use with caution'
               f'.{Ct.a}',
        add_help=True,
    )
    parser.add_argument(
        '-f',
        '--file',
        help='file to generate hash against',
        metavar=f'{Ct.red}<filename>{Ct.a}',
        type=str,
    )
    parser.add_argument(
        '--hash',
        help='hash type to use; ignored if all is used',
        metavar=f'{Ct.yellow}<hash>{Ct.a}',
        type=str,
        default='sha256',
    )
    parser.add_argument(
        '-l',
        '--length',
        help='"shake" hash requires digest length value (1-128)',
        metavar=f'{Ct.yellow}<number>{Ct.a}',
        type=int,
        default=32,
    )
    parser.add_argument(
        '--all',
        help='run all available hashes against file; cannot be used with --compare',
        action='store_true',
    )
    parser.add_argument(
        '--available',
        help='print available hashes, their values, and exit',
        action='store_true',
    )
    parser.add_argument(
        '-b',
        '--blocksize',
        help='specify number of 1kB read blocks (1-1000000);consumes more ram for '
             'minimally faster processing',
        metavar=f'{Ct.yellow}<number>{Ct.a}',
        type=int,
        default=16,
    )
    parser.add_argument(
        '-c',
        '--compare',
        help='value to compare against generated hash; cannot be used with --all',
        metavar=f'{Ct.yellow}<value>{Ct.a}',
        type=str,
    )
    parser.add_argument(
        '--no-color',
        help='don\'t colorize output',
        action='store_true',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='display additional details',
        action='count',
        default=0,
    )
    parser.add_argument(
        '--version',
        help='print program version and exit',
        action='version',
        version=f'{Ct.bblue}{ver}{Ct.a}',
    )

    return parser.parse_args()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def validate_and_process_args(hash_list: list):
    """Validate and process the cli args before executing main()."""
    # ~~~ #                 -length & blocksize-
    if args.length < 1 or args.length > 128:
        bp([f'"--length {args.length}" invalid. Length must be between (and '
            'including) 1 and 128.', Ct.red], err=2)
        sys.exit(1)
    if args.blocksize < 1 or args.blocksize > 1000000:
        bp([f'"--blocksize {args.blocksize}" invalid. Length must between (and'
            ' including) 1 and 1000000.', Ct.red], err=2)
        sys.exit(1)

    # ~~~ #                 -available-
    if args.available:
        bp(['Available:\nHash:\t\tBlock size:\tDigest Length:\tHex Length:',
            Ct.a])
        for i in hash_list:
            if 'shake' not in i:
                bp([f'{i:<16s}', Ct.red,
                    f'{getattr(hashlib, i)().block_size:<16}'
                    f'{getattr(hashlib, i)().digest_size:<16}'
                    f'{2 * getattr(hashlib, i)().digest_size:<16}', Ct.bblue],
                    num=0)
            else:
                bp([f'{i:<16s}', Ct.red,
                    f'{getattr(hashlib, i)().block_size:<16}{args.length:<16}'
                    f'{2 * args.length:<16}', Ct.bblue], num=0)
        sys.exit(0)

    # ~~~ #                 -file-
    if args.file:
        if not os.path.isfile(args.file):
            bp([f'"--file {args.file}" does not exist.', Ct.red], err=2)
            sys.exit(1)
    else:
        bp(['no file specified.', Ct.red], err=2)
        sys.exit(1)

    # ~~~ #                 -all-
    if not args.all:
        if args.hash.lower() not in hash_list:
            bp([f'"--hash {args.hash}" invalid or unavailable.', Ct.red],
               err=2)
            sys.exit(1)
        else:
            hash_list = [args.hash.lower()]

    # ~~~ #                 -compare-
    if args.compare and args.all:
        bp(['cannot combine "--compare" with "--all".', Ct.red], err=2)
        sys.exit(1)

    return hash_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def byte_notation(size: int, acc=2, ntn=0):
    """Decimal Notation: take an integer, converts it to a string with the
    requested decimal accuracy, and appends either single (default), double,
    or full word character notation.

    - Args:
        - size (int): the size to convert
        - acc (int, optional): number of decimal places to keep. Defaults to 2.
        - ntn (int, optional): notation name length. Defaults to 0.

    - Returns:
        - [tuple]: 0 = original size int unmodified; 1 = string for printing
    """
    size_dict = {
        1: ['B', 'B', 'bytes'],
        1000: ['k', 'kB', 'kilobytes'],
        1000000: ['M', 'MB', 'megabytes'],
        1000000000: ['G', 'GB', 'gigabytes'],
        1000000000000: ['T', 'TB', 'terabytes'],
    }
    return_size_str = ''
    for key, value in size_dict.items():
        if (size / key) < 1000:
            return_size_str = f'{size / key:,.{acc}f} {value[ntn]}'
            return size, return_size_str


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def file_read(file_handle, file_blocks):
    """A simple function to read a part of a file in chunks. It is decorated
    with a timer to track duration.

    - Args:
        - file_handle (file): the open file to read
        - file_blocks (file): the size in bytes to read

    - Returns:
        - [file]: returns the read blocks
    """
    return file_handle.read(file_blocks)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def hash_processing(hash_str, hash_action, hlib, file_blocks=0):
    """This hashes a block of a file (or whole file if small enough). The
    hashlib must be passed back and forth to maintain a single, consistant
    hashlib to update for files bigger than the block size. This will also
    generate a hexadecimal output of a hashlib.

    - Args:
        - hlib (hashlib): the hashlib to update
        - hash_action (str): either 'update' to runs hashlib.update or 'hex' to
                             run hashlib.hexdigest.
        - file_blocks (int, optional): required for hash_action of 'update';
                                       the data to hash. Defaults to 0.

    - Returns:
        - [hashlib]: for 'update' hash action, returns an updated hashlib
                     object,for 'hex' hash action, returns a hexadecimal
                     string.
    """
    # ~~~ #         update section
    if hash_action == 'update':
        return hlib.update(file_blocks)
    # ~~~ #         hex section
    elif hash_action == 'hex':
        if 'shake' in hash_str:
            return hlib.hexdigest(args.length)
        else:
            return hlib.hexdigest()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hash_check(h_list: list):
    """This function reads the file in chunks and executes the hashing
       algorithm. This tracks the file read times along with the hashing time.

    Args:
        - h (str): this is the type of hash to execute on this function

    Returns:
        - tuple: the time to read the file, the time to hash the file, and the
               standard hexadecimal hash output of the requested type.
    """
    try:
        # ~~~ #                 -variables-
        hr_dict = {
            'failure': 0,
            'file_source': args.file,
            'short_source': (
                args.file
                if len(args.file) < 63
                else f'...{args.file[(len(args.file) - 60):]}'
            ),
            'read_blocks': args.blocksize * BLOCK_SIZE_FACTOR,
            'file_size': os.stat(args.file, follow_symlinks=False).st_size,
            'file_read_time': 0.0,
            'hash_list': h_list,
            'hash_time': {},
            'hash_hex': {},
        }
        # this holds one or all of the hashlibs
        hlib_dict = {}
        for h in h_list:
            hlib_dict[h] = getattr(hashlib, h)()
            hr_dict['hash_time'][h] = 0
            hr_dict['hash_hex'][h] = ''
        # loop tracker for realtime progress
        file_loop = 0
        # number of loops to execute
        file_loops = ceil(hr_dict['file_size'] / hr_dict['read_blocks'])
        # limit cli output to max of 100 loops to prevent slowdown
        update_loop = 1 if file_loops < 100 else int(file_loops / 100)

    # ~~~ #                 -file open-
        with open(hr_dict['file_source'], 'rb') as f:
            while True:
                # read source in blocks to prevent potential memory overload
                f_chunk = file_read(f, hr_dict['read_blocks'])
                hr_dict['file_read_time'] += f_chunk[1]
                # this breaks the while loop when file chunk is empty
                if not f_chunk[2]:
                    # ensure 100% when complete and add line breaks
                    bp(['\u001b[1000D100%', Ct.bblue, ' | ', Ct.a,
                        f'{hr_dict["short_source"]}\n', Ct.green], log=0,
                        num=0, fil=0, veb=1)
                    break
                # send this chunk to be hashed by each algorithm
                for k, v in hlib_dict.items():
                    hash_return = hash_processing(k, 'update', v, f_chunk[2])
                    hr_dict['hash_time'][k] += hash_return[1]
                # loop increment and output status
                file_loop += 1
                if file_loop % update_loop == 0:
                    bp([f'\u001b[1000D{(file_loop / file_loops) * 100:.0f}%',
                        Ct.bblue, ' | ', Ct.a, f'{hr_dict["short_source"]}',
                        Ct.green], log=0, inl=1, num=0, fls=1, fil=0, veb=1)
            # convert hashes into standard hexadecimal notation
            for k, v in hlib_dict.items():
                hash_return = hash_processing(k, 'hex', v)
                hr_dict['hash_time'][k] += hash_return[1]
                hr_dict['hash_hex'][k] = hash_return[2]
        return hr_dict

    except OSError as e:
        bp([f'with file read: {hr_dict["file_source"]}\n{e}', Ct.red], err=2)
        hr_dict['failure'] = 1
        return hr_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main(h_list: list):

    # ~~~ #                 -verbose init-
    bp([f'Python: v{platform.python_version()} | '
        f'{platform.python_implementation()} | '
        f'{platform.python_compiler()}', Ct.a], veb=1, log=0)
    bp([f'OS: {platform.platform()} | {platform.processor()}', Ct.a], veb=1,
        log=0)
    bp(['Args: ', Ct.a], inl=1, veb=1, log=0)
    for k, v in vars(args).items():
        if k == 'hash':
            bp([f'{k}: ', Ct.a, f'{v}', Ct.red, ' | ', Ct.a],
                num=0, inl=1, veb=1, log=0)
        elif k == 'compare':
            bp([f'{k}: {v} | ', Ct.a], num=0, inl=1, veb=1,
                log=0)
        else:
            bp([f'{k}: ', Ct.a, f'{v}', Ct.green, ' | ', Ct.a], inl=1, veb=1,
                log=0)
    bp(['\u001b[1D \n', Ct.a], veb=1, log=0, num=0)

    # ~~~ #                 -hash-
    hash_dict = hash_check(hash_list)

    # ~~~ #                 -read output-
    cumulative_time = hash_dict['file_read_time']
    read_speed = hash_dict["file_size"] / hash_dict['file_read_time']
    bp([f'Size: {byte_notation(hash_dict["file_size"], ntn=1)[1]} | '
        f'Read Time: {hash_dict["file_read_time"]:.4f} | '
        f'Read Speed: {byte_notation(read_speed, ntn=1)[1]}/s', Ct.a])

    # ~~~ #                 -hash output-
    bp(['\nHash:\t\tHash Time:\tHash Speed:\tHex Value:', Ct.a])
    for i in hash_dict['hash_list']:
        h_time = f'{hash_dict["hash_time"][i]:.4f}s'
        h_speed = int(hash_dict["file_size"] / hash_dict["hash_time"][i])
        h_speed = f'{byte_notation(h_speed, ntn=1)[1]}/s'
        bp([f'{i:<16s}', Ct.red, f'{h_time:<16}', Ct.bblue, f'{h_speed:<16}',
            Ct.bblue, f'{hash_dict["hash_hex"][i]}', Ct.a], num=0)
        cumulative_time += hash_dict["hash_time"][i]

    # ~~~ #                 -compare-
    if args.compare:
        bp([f'\nGenerated: {hash_dict["hash_hex"][h_list[0]]}', Ct.a], num=0)
        if hash_dict["hash_hex"][h_list[0]] == args.compare:
            bp([f' Compared: {args.compare}\n', Ct.a, 'HASHES MATCH!!',
                Ct.green], num=0)
        else:
            bp([f'Compared:  {args.compare}\n', Ct.a, 'HASHES DO NOT MATCH!!',
                Ct.red], num=0)

    # ~~~ #                 -verbose end-
    end_time = perf_counter()
    total_time = end_time - START_PROG_TIME
    bp(['', Ct.a], log=0, veb=1)
    bp([f'{total_time:.4f}s - Total Time', Ct.a], veb=1, log=0)
    bp([f'{total_time - cumulative_time:.4f}s - Program Overhead Time', Ct.a],
        veb=1, log=0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    # ~~~ #             -class variables-
    Ct = ColorText()
    Ct.a = '\u001b[0m'
    Ct.red = '\u001b[38;5;1m'
    Ct.green = '\u001b[38;5;2m'
    Ct.yellow = '\u001b[38;5;3m'
    Ct.bblue = '\u001b[38;5;12m'
    Ct.bmagenta = '\u001b[38;5;13m'
    Ct.grey1 = '\u001b[38;5;255m'
    Ct.orange = '\u001b[38;2;233;133;33m'

    # ~~~ #             -args-
    args = get_args()

    # ~~~ #             -validate-
    validate_and_process_args(hash_list)

    # ~~~ #             -variables-
    hash_list = hash_list if args.all else [args.hash]
    bp_dict['verbose'] = args.verbose

    # ~~~ #             -title-
    bp([f'{ver}: {__purpose__}\n', Ct.bblue])

    main(hash_list)
