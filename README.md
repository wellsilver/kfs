keep in sync with github/wellsilver/kfs

# kfs

big fancy tree

little endian

simple (hopefully)

btw theres tables in kfs.h of all this stuff

## overview
| start | end | desc |
| ----- | ----- | - |
| 1 | 5 | 5 sectors of 2.56 kilobytes for any bios bootloader |
| 6 | 6 | fs extender |
| 7 | 7 | "/" or first folder |
| 8 | 10| reserved |
| 11 | ? | data |

a driver would be keeping the first 10 sectors in memory

### fs extender
unused rn

this is for extending the fs past its actual hard drive

like an entry in here would say that "sectors" 0-500 is the hard drive at sata:0

another entry would say that "sectors" 501-600 is a specific file on a ftp server

each entry is 64 bytes long leaving 8 entries

empty entrys have the first byte as zero

if blank set first entry type enum to 254

#### entry
| start | end | type | desc |
| ----- | --- | ---- | ---- |
| 0 | 0 | u8  | type enum   |
| 1 | 8 | u64 | start sector|
| 9 | 17| u64 | end sector  |
| 11| 63| ... | type specific data |

#### type enum
| num | desc |
| --- | ---- |
| 0   | empty |
| 1   | drive |
| 254 | blank |
..


### folders

descriptor, supposed to first
| type | desc |
| ---- | ---- |
| u8   | type=1 |
| u64  | previous sector (of the folder) |
| u64  | next sector (of the folder) |

file - gives the sector where the file descriptor is
| type | desc |
| ---- | ---- |
| u8   | type=2 |
| u64  | sector of file descriptor |
| u128 | hash of first file descriptor sector |

directory - gives the sector where the first sector of directory is
| type | desc |
| ---- | ---- |
| u8   | type=3 |
| u64  | first sector of directory |
| u128 | hash of first sector of directory |

### file
