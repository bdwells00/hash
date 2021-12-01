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
  
#### Minimum usage example:
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

#### Comparison example:
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

#### All hash with L1 verbosity example:
```
  hash.py -f /Linux/alpine-extended-3.15.0-x86_64.iso --all -v
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

Python: v3.10.0 | CPython | MSC v.1929 64 bit (AMD64)
OS: Windows-10-10.0.22000-SP0 | AMD64 Family 23 Model 96 Stepping 1, AuthenticAMD
Args:  file: \Linux\alpine-extended-3.15.0-x86_64.iso | hash:sha256 | length: 32 | all: True | available: False | blocksize: 16 | compare: None | no_color: False | verbose: 1

100% | Hash: blake2b   | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: blake2s   | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: md5       | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha1      | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha224    | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha256    | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha384    | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_224  | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_256  | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_384  | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_512  | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha512    | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: shake_128 | File: \Linux\alpine-extended-3.15.0-x86_64.iso
100% | Hash: shake_256 | File: \Linux\alpine-extended-3.15.0-x86_64.iso

Hash:       File Time:  Hash Time:      Hex Value:
blake2b     0.2370s     1.2160s         bbf173718952406b91632c741a892d4f787efea31854d1f07bd178d4a924332320a09fb9c6876f203337930f3722a1ac07a6c3ec32cf397eeb0a56c787d7eda6
blake2s     0.3430s     1.7350s         8a1aad2d544d2af01d64e4925a889c6ccee16bf96f853ae7536f72cd5facc91c
md5         0.2500s     0.9530s         de72fa9e5f727b03f9a03e27affc70b7
sha1        0.2670s     0.3580s         4babcc407aecfd25ceddd2a038aadab5a8a6b106
sha224      0.3100s     0.3930s         9d9bbffbda16bedd05dc05976c3cdb940b1939dba87f5e35b695e91b
sha256      0.3270s     0.3770s         3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
sha384      0.2830s     0.8420s         5a53fa6e189c53028bf5ef0ddc0b8d29ba89b647d9ada3fcdfc5690312af7942329b2f47a92cd74bfe818e2619b49f1f
sha3_224    0.3260s     1.4080s         f18facfe594e273587b1e2d7527d8298460595c1efd3776a95bd7540
sha3_256    0.3270s     1.4070s         39a46701a7fc5b63e78bfaa417905e34bbaa21d029ef01da2e96e50091be348e
sha3_384    0.2820s     1.9670s         3c3eb58b3ecc6375cf55b2ef632ea064dd7554c9dbd1369ef93c9921a9aa98e8ea069a5ec16d0a7afdb77f1f8033ee2b
sha3_512    0.2830s     2.6580s         c171fc4057e8a14c4a46d16e17c28a8d0bcb0325fe87430a9133ddd1091c2e2fff0a2212cd03a116d15e535607fde0ed514350a62dfd53bb39273e288f83e321
sha512      0.2670s     0.8580s         56cbd835c874d2cc73c2668a8803fdbd7a88fc8947306146f704e6075885723e72b98cd6bf667944025f94d27d55fe0fda13bc0a43a59a5668a380898d9af626
shake_128   0.2520s     1.3250s         590104870ac3a495a2b849b1741e125c843036c7d75e9f91f132362e6a04f65e
shake_256   0.2810s     1.4690s         f345184e9895af3edf513ebfe660179e693eba15c2390239bd15dd1e4eb30249

program total time:    21.562000000150874s
program overhead time: 0.5609999999869615s
```

#### The same All hash with L1 verbosity on a slightly faster linux server example:
```
  python3 ./hash.py -f ./alpine-extended-3.15.0-x86_64.iso -v --all
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

Python: v3.9.7 | CPython | GCC 11.2.0
OS: Linux-5.15.3-051503-generic-x86_64-with-glibc2.34 | x86_64
Args:  file: ./alpine-extended-3.15.0-x86_64.iso | hash:sha256 | length: 32 | all: True | available: False | blocksize: 16 | compare: None | no_color: False | verbose: 1

100% | Hash: blake2b   | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: blake2s   | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: md5       | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha1      | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha224    | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha256    | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha384    | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_224  | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_256  | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_384  | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha3_512  | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: sha512    | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: shake_128 | File: ./alpine-extended-3.15.0-x86_64.iso
100% | Hash: shake_256 | File: ./alpine-extended-3.15.0-x86_64.iso

Hash:       File Time:  Hash Time:      Hex Value:
blake2b     0.1580s     0.8124s         bbf173718952406b91632c741a892d4f787efea31854d1f07bd178d4a924332320a09fb9c6876f203337930f3722a1ac07a6c3ec32cf397eeb0a56c787d7eda6
blake2s     0.1571s     1.2121s         8a1aad2d544d2af01d64e4925a889c6ccee16bf96f853ae7536f72cd5facc91c
md5         0.1564s     0.8041s         de72fa9e5f727b03f9a03e27affc70b7
sha1        0.1497s     0.3554s         4babcc407aecfd25ceddd2a038aadab5a8a6b106
sha224      0.1503s     0.3758s         9d9bbffbda16bedd05dc05976c3cdb940b1939dba87f5e35b695e91b
sha256      0.1506s     0.3757s         3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
sha384      0.1551s     0.7263s         5a53fa6e189c53028bf5ef0ddc0b8d29ba89b647d9ada3fcdfc5690312af7942329b2f47a92cd74bfe818e2619b49f1f
sha3_224    0.1573s     1.1627s         f18facfe594e273587b1e2d7527d8298460595c1efd3776a95bd7540
sha3_256    0.1573s     1.2283s         39a46701a7fc5b63e78bfaa417905e34bbaa21d029ef01da2e96e50091be348e
sha3_384    0.1597s     1.5075s         3c3eb58b3ecc6375cf55b2ef632ea064dd7554c9dbd1369ef93c9921a9aa98e8ea069a5ec16d0a7afdb77f1f8033ee2b
sha3_512    0.1591s     2.1435s         c171fc4057e8a14c4a46d16e17c28a8d0bcb0325fe87430a9133ddd1091c2e2fff0a2212cd03a116d15e535607fde0ed514350a62dfd53bb39273e288f83e321
sha512      0.1558s     0.7263s         56cbd835c874d2cc73c2668a8803fdbd7a88fc8947306146f704e6075885723e72b98cd6bf667944025f94d27d55fe0fda13bc0a43a59a5668a380898d9af626
shake_128   0.1569s     1.0148s         590104870ac3a495a2b849b1741e125c843036c7d75e9f91f132362e6a04f65e
shake_256   0.1577s     1.2287s         f345184e9895af3edf513ebfe660179e693eba15c2390239bd15dd1e4eb30249

program total time:    17.332667410984868s
program overhead time: 1.4780595321499277s

```

#### Available hash example:
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


## Comparison with other tools

#### Linux (Ubuntu server 21.10) putty 0.76 - sha256sum (GNU coreutils 8.32) using GNU Time:
```
  /usr/bin/time sha256sum alpine-extended-3.15.0-x86_64.iso
```
Output:
```
3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3  alpine-extended-3.15.0-x86_64.iso
1.84user 0.09system 0:01.93elapsed 100%CPU (0avgtext+0avgdata 2324maxresident)k
0inputs+0outputs (0major+111minor)pagefaults 0swaps
```
#### Linux (Ubuntu server 21.10) putty 0.76 - hash.py (1.4.6) using GNU Time:
```
  /usr/bin/time python3 ./hash.py -f ./alpine-extended-3.15.0-x86_64.iso -v
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

Python: v3.9.7 | CPython | GCC 11.2.0
OS: Linux-5.15.3-051503-generic-x86_64-with-glibc2.34 | x86_64
Args:  file: ./alpine-extended-3.15.0-x86_64.iso | hash:sha256 | length: 32 | all: False | available: False | blocksize: 16 | compare: None | no_color: False | verbose: 1

100% | Hash: sha256    | File: ./alpine-extended-3.15.0-x86_64.iso

Hash:       File Time:  Hash Time:      Hex Value:
sha256      0.1494s     0.3769s         3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3

program total time:    0.6363643319928087s
program overhead time: 0.1100371487555094s
0.41user 0.24system 0:00.66elapsed 100%CPU (0avgtext+0avgdata 14324maxresident)k
0inputs+0outputs (0major+3413minor)pagefaults 0swaps
```
#### Windows (11) certutil (10.0.22000.1) Terminal Preview 1.12.2931 - PS 7.2 using Measure-Command:
```
  Measure-Command { certutil.exe -hashfile \Linux\alpine-extended-3.15.0-x86_64.iso sha256 | Out-Default }
```
Output:
```
SHA256 hash of \Linux\alpine-extended-3.15.0-x86_64.iso:
3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3
CertUtil: -hashfile command completed successfully.

Days              : 0
Hours             : 0
Minutes           : 0
Seconds           : 0
Milliseconds      : 612
Ticks             : 6120578
TotalDays         : 7.08400231481482E-06
TotalHours        : 0.000170016055555556
TotalMinutes      : 0.0102009633333333
TotalSeconds      : 0.6120578
TotalMilliseconds : 612.0578
```
#### Windows (11) hash.py (1.4.6) Terminal Preview 1.12.2931 - PS 7.2 using Measure-Command:
```
  Measure-Command { .\hash.py -f \Linux\alpine-extended-3.15.0-x86_64.iso -v | Out-Default }
```
Output:
```
hash.py v1.4.6 (2021-12-01): Calculate hash codes for files.

Python: v3.10.0 | CPython | MSC v.1929 64 bit (AMD64)
OS: Windows-10-10.0.22000-SP0 | AMD64 Family 23 Model 96 Stepping 1, AuthenticAMD
Args:  file: \Linux\alpine-extended-3.15.0-x86_64.iso | hash:sha256 | length: 32 | all: False | available: False | blocksize: 16 | compare: None | no_color: False | verbose: 1

100% | Hash: sha256    | File: \Linux\alpine-extended-3.15.0-x86_64.iso

Hash:       File Time:  Hash Time:      Hex Value:
sha256      0.2200s     0.3730s         3d78e47400176622ce5846139708d1eadb890de1c430c982a9f6548a446e78b3

program total time:    0.6879999998491257s
program overhead time: 0.09499999973922968s

Days              : 0
Hours             : 0
Minutes           : 0
Seconds           : 0
Milliseconds      : 776
Ticks             : 7760233
TotalDays         : 8.98175115740741E-06
TotalHours        : 0.000215562027777778
TotalMinutes      : 0.0129337216666667
TotalSeconds      : 0.7760233
TotalMilliseconds : 776.0233
```

### Table of results
| OS    | CPU   |  Program | Time  | hash.py time |
| :---: | :---: | :------: | :---: | :----------: |
| Ubuntu 21:10 (5.15 kernel) | AMD Ryzen 5 5600G | sha256sum (8.32) | 1.93s | n/a |
| Ubuntu 21:10 (5.15 kernel) | AMD Ryzen 5 5600G | hash.py (1.4.6) | 0.66s | 0.64s |
| Windows 11 21H2 (22000.318)) | AMD Ryzen 7 4700U | certutil (10.0.22000.1) | 0.61s | n/a |
| Windows 11 21H2 (22000.318)) | AMD Ryzen 7 4700U | hash.py (1.4.6) | 0.77s | 0.69s |

## Minutiae
  
  * To maintain 3.6 compatibility, timing uses monotonic instead of the more precise 3.7 monotonic_ns (float free).
  * Use --available to see all the available hash algorithms on the python platform. This also shows the internal blocksize, the digest size, and the Hex output length for each hash.
  * The shake hashes require a length variable. The default value of 32 has a 64 character hex output length (matching sha256's output length). Regardless of length specified, the output is always the same up to the point of cutoff (the 2 characters for length 1 match the first 2 characters for length 32).
  * The file that gets hashed is read in chunks as a tuneable multiplier (--blocksize) of 1000. The default value of 16 (16kB or 16,000), seems sufficient due to diminishing returns of fractional seconds. A maximum value of 100,000,000 (100GB) can be requested though you are likely to run out of ram.
  * To accommodate time tracking, the file is re-read through every hash when using --all.
  * Three levels of verbosity has been implemented. -v is useful to see more details (platform, OS, args, program total time & program overhead time), -vv will provide a little more detail, and -vvv is debug level where essentially all comments where turned into level 3 print statements for an ungodly amount of output.
  * Color output has been implemented and looks acceptable on typical light and dark backgrounds. Use --no-color to disable if it's bothersome or unusable for certain color 
