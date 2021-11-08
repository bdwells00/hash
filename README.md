# hash
Use python to generate hexadecimal hash codes

The minimum Python version is 3.6 due to f-strings. This should be compatible with 3.6+.

This only uses builtin modules with no pip installs required.

Modules used:
* argparse
* collections
* hashlib
* os
* platform
* sys
* time


## Usage

usage: hash.py [-h] [-f <filename>] [--hash <hash>] [-l <number>] [--all] [-a] [-b <number>] [-v] [--version]

hash.py v1.0.0 (2021-11-07): Calculate hash codes for files

optional arguments:
  -h, --help            show this help message and exit
  -f <filename>, --file <filename>
                        file to generate hash against (default: None)
  --hash <hash>         hash type to use (default: sha256)
  -l <number>, --length <number>
                        "shake" hash requires a length value (default: 32)
  --all                 run all available hashes against file (default: False)
  -a, --available       print available hashes and their blocksizes (default: False)
  -b <number>, --blocksize <number>
                        specify file read blocksize multiplier (consumes more ram) (default: 128)
  -v, --verbose         provide additional details (default: False)
  --version             print program version and exit

This program has no warranty. Please use with caution.

  
Minimum usage example:
  hash.py -f hash.py
Output:
  Hash:       Time:       Hex Value:
  sha256      0.0000s     4cca846639cfc4dd3b1be5c9e48e2f9aa3fbfc3d16f134bf187560a4fc01eacf

## Minutiae
  
  * To maintain 3.6 compatibility, timing uses monotonic instead of the more precise 3.7 monotonic_ns (float free).
  * Use -a to see all the available hash algorithms on the python platform. This also shows the internal blocksize of each, and the digest size (output). Double the digest size to get the output hex length.
  * The shake hashes require a length variable (this is a tuneable digest size which is why it shows '0' for --a). The default value of 32 has a 64 character hex output length (like sha256's output length). Regardless of length specified, the output is always the same up to the point of cutoff (the 2 characters for length 1 match the first 2 characters for length 32).
  * The file that gets hashed is read in chunks as a tuneable multiplier (blocksize argument) of the hash algorithm's blocksize. The default value of 128 seems sufficient due to diminishing returns of fractional seconds.
  * To accommodate time tracking, the file is re-read through every hash when using --all. A future rewrite may send each chunk into separate hash variables before moving on to the next chunk to reduce file reads and attempt to sum the individual chunks of each. This may cause the first hash to be slightly slower than the rest due to OS or disk caching.  When comparing, discard the first run and take a mean average of several runs.
  * Verbose will give additional platform details for speed comparison
