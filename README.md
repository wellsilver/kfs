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
todo

### folder descriptor

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

### file descriptor
