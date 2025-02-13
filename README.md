keep in sync with github/wellsilver/kfs

# kfs

big fancy tree

little endian

simple (hopefully)

hashes are cityhash128 and are optional (set to 0 if not present)

sectors start from 1, 0 is a invalid sector.

btw theres tables in kfs.h of all this stuff which are probably easier to use and read

kfs.h also has a dependency-less implementation of cityhash128 if you need it ``void kfscityhash128(char *in, int size, char out[16])``

### kfs.py
tool for working with kfs image files

python kfs.py -f out.kfs -c -add filename1 -add filename2

also works as a library

### basic driver
examples kfs.c and kfs.S

read first sector, and use its table to verify

## overview
| size (sectors) | desc |
| - | - |
| 5 | 2.56 kilobytes for bootloader |
| 1 | fs extender |
| 1 | "/" or first folder |
| 1 | folder "garbage bin" |
| 2 | reserved |
| ? | data |

### garbage bin
- holds all free sectors
- empty space are unnamed files
- when files are deleted they can appear in the "garbage bin" and are counted as free space, but can be restored

all files in the garbage bin are free data (but if they are named, they should be removed when used)

### table in first sector

everything after this table can be code
| type  | desc |
| ----- | ---- |
| 3byte | jmp to code, nop |
| 3byte | "KFS" |
| u16   | version = 2 |
| u64   | sector of the file descriptor of a highlighted file |

### fs extender
todo

### folder
every entry is 25 bytes

descriptor, supposed to first in every sector
| type | desc |
| ---- | ---- |
| u8   | type=1 |
| u64  | previous sector (of the folder) |
| u64  | next sector (of the folder) |
| u64  | sector where the folders name is |

file - gives the sector where the file descriptor is
| type | desc |
| ---- | ---- |
| u8   | type=2 |
| u64  | sector of file descriptor sector |
| u128 | hash of file descriptor sector |

directory - gives the sector where the first directory sector is
| type | desc |
| ---- | ---- |
| u8   | type=3 |
| u64  | sector of first directory sector |
| u128 | hash of first directory sector |

### file descriptor
a header then a table of where file data is
| type | desc |
| ---- | ---- |
| str40| name |
| u64  | epoch creation |
| u64  | epoch last modification |
| u64  | epoch last read |
| u64  | size in bytes      |
| u8   | compression type   |
| u8   | encryption type    |

^len of the table is 74

after the header is all file data entry's

next sector descriptor, the next sector has no header and is a direct continuation of the last entry of the current table
| type | desc |
| ---- | ---- |
| u64  | set to 0 |
| u64  | the next sector |
| u128 | hash of the next sector |

data descriptor start,end is a range of sectors.
| type | desc |
| ---- | ---- |
| u64  | start sector |
| u64  | end sector   |
| u128 | hash of data |