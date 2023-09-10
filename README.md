# kfs

big fancy tree

simple (hopefully)

## overview
LBA
| start | end | desc |
| ----- | ----- | - |
| 1 | 5 | 5 sectors of 2.56 kilobytes for bootloader |
| 6 | 6 | fs extender |
| 7 | 7 | "/" or first folder |
| 8 | 10| reserved |
| 11 | ? | data |

a driver would be keeping the first 10 sectors in memory

### fs extender
this is for extending the fs past its actual hard drive

like an entry in here would say that "sectors" 0-500 is the hard drive at sata:0

another entry would say that "sectors" 501-600 is a specific file on a ftp server

each entry is 32 bytes long leaving 16 entries

empty entrys have the first byte as zero

for the primary drive only type, start sector, end sector is used

#### entry
| start | end | type | desc |
| ----- | --- | ---- | ---- |
| 0 | 0 | u8  | type enum   |
| 1 | 5 | u32 | start sector|
| 6 | 10| u32 | end sector  |
| 11| 32| ... | type specific data |

#### type enum
| num | desc |
| --- | ---- |
| 0   | empty |
| 1   | drive |
..


### folders

folders contain entrys that point to other files or folders

#### type enum
| num | desc |
| --- | ---- |
| 0   | empty |
| 1   | descriptor |
| 2   | filedesc  |
| 3   | filedata  |/
| 4   | folder|

#### entry
all entrys are 32 bytes large

all
| start | end | type | desc |
| ----- | --- | ---- | ---- |
| 0     | 0   | u8   | type enum |

descriptor - folders cant be of a finite size, this will point to the previous sector for the folder (or 0 if nil) and the next sector of the folder (or 0 if nil) this should be the first entry
| start | end | type | desc |
| ----- | --- | ---- | ---- |
| 1     | 8   | u64  | previous sector |
| 9     | 17  | u64  | next sector |
| 18    | 31  | ?    | unused |

filedata - gives a range of sectors associated with a file through a fileID
| start | end | type | desc |
| ----- | --- | ---- | ---- |
| 1     | 8   | u64  | first sector in range |
| 9     | 17  | u64  | last sector in range  |
| 18    | 20  | u16  | fileID |
| 21    | 24  | u32  | 