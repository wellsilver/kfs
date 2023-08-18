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
| 11| 32| any | type specific data |

#### type enum
| num | desc |
| --- | ---- |
| 0   | empty |
| 1   | primary drive |
..


### folders
