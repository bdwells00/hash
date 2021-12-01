# hash
Use python to generate hexadecimal hash codes.

The minimum Python version is 3.6 due to f-strings. This should be compatible with 3.6+.

This only uses builtin modules with no pip installs required.

Modules used:
* argparse
* collections
* datetime
* hashlib
* math
* os
* platform
* sys
* time


## Usage

```
usage: hash.py [-h] -f <filename> [--hash <hash>] [-l <number>] [--all]
               [--available] [-b <number>] [-c <value>] [--no-color] [-v] [--version]

hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

options:
  -h, --help            show this help message and exit
  -f <filename>, --file <filename>
                        file to generate hash against (default: None)
  --hash <hash>
                        hash type to use; ignored if all is used (default: sha256)
  -l <number>, --length <number>
                        "shake" hash requires a digest length value (1-128); ignored for all other hashes (default:
                        32)
  --all                 run all available hashes against file; cannot be used with --compare (default: False)
  --available           print available hashes, their values, and exit (default: False)
  -b <number>, --blocksize <number>
                        specify number of 1kB read blocks (1-100000000);consumes more ram for minimally faster
                        processing (default: 16)
  -c <value>, --compare <value>
                        value to compare against generated hash; cannot be used with --all (default: None)
  --no-color            don't colorize output (default: False)
  -v, --verbose         3 lvl incremental verbosity (-v, -vv, or -vvv) (default: 0)
  --version             print program version and exit

This program has no warranty. Please use with caution.
```
  
Minimum usage example:
```  
  hash.py -f hash.py
```  
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

100% | Hash: sha256    | File: ./hash.py

Hash:       File Time:  Hash Time:      Hex Value:
sha256      0.0000s     0.0000s         8c40f88e554f5f51cf12ecc99c3bee8d80deabfaa1b6bcfa4c29760d4d49eb3d
```

Comparison example:
```
  hash.py -f /Linux/alpine-extended-3.15.0-x86_64.iso --compare 3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

100% | Hash: sha256    | File: /Linux/alpine-extended-3.15.0-x86_64.iso

Hash:       File Time:  Hash Time:      Hex Value:
sha256      0.3140s     0.3750s         3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3

Generated: 3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
Compared:  3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
HASHES MATCH!!
```

Available hash example:
```
  hash.py --available
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

Available:
Hash:           Block size:     Digest Length:  Hex Length:
blake2b         128             64              128
blake2s         64              32              64
md5             64              16              32
sha1            64              20              40
sha224          64              28              56
sha256          64              32              64
sha384          128             48              96
sha3_224        144             28              56
sha3_256        136             32              64
sha3_384        104             48              96
sha3_512        72              64              128
sha512          128             64              128
shake_128       168             32              64
shake_256       136             32              64
```

## Minutiae
  
  * To maintain 3.6 compatibility, timing uses monotonic instead of the more precise 3.7 monotonic_ns (float free).
  * Use --available to see all the available hash algorithms on the python platform. This also shows the internal blocksize, the digest size, and the Hex output length for each hash.
  * The shake hashes require a length variable. The default value of 32 has a 64 character hex output length (matching sha256's output length). Regardless of length specified, the output is always the same up to the point of cutoff (the 2 characters for length 1 match the first 2 characters for length 32).
  * The file that gets hashed is read in chunks as a tuneable multiplier (--blocksize) of 1000. The default value of 16 (16kB or 16,000), seems sufficient due to diminishing returns of fractional seconds. A maximum value of 100,000,000 (100GB) can be requested though you are likely to run out of ram.
  * To accommodate time tracking, the file is re-read through every hash when using --all.
  * Three levels of verbosity has been implemented. -v is useful to see more details (platform, OS, args, program total time & program overhead time), -vv will provide a little more detail, and -vvv is debug level where essentially all comments where turned into level 3 print statements for an ungodly amount of output.
  * Color output has been implemented and looks acceptable on typical light and dark backgrounds. Use --no-color to disable if it's bothersome or unusable for certain color 
