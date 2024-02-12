# utility for creating kfs2 discs.. until kfs.py is finished

# python format.py *name* *sizeinsectors* *bootsector file or 0* *files, first of which is highlighted*
# python format.py test.bin 128 kernel.abc
from sys import argv
import time

name = argv[1]
size = int(argv[2])
boots = argv[3]
nobootsector = True
if argv[3]!='0':
  boots=open(argv[3],'r')
  nobootsector=False
files_, files = []
try:
  files_= argv[4:]
except IndexError: pass # ignore

sizeneeded = 11
for i in files_:
  i = open(i, 'r')
  files.append(i)

def _makefileheader(name:bytes, size:int, creation=int(time.time()), modification=int(time.time()), lastread=int(time.time())) -> bytes:
  ret = b""
  ret += name.ljust(40, b'\0') # name

  ret += creation.to_bytes(length=8,byteorder='little') # epoch creation
  ret += modification.to_bytes(length=8,byteorder='little') # epoch last modification
  ret += lastread.to_bytes(length=8,byteorder='little') # epoch last read
  ret += size.to_bytes(length=8,byteorder='little') # size in bytes

  ret += (0).to_bytes(byteorder='little')
  ret += (0).to_bytes(byteorder='little')
  return ret

def _makedirfileentry(pos:int, hash_=0):
  return b""+(2).to_bytes(byteorder='little')+pos.to_bytes(length=8,byteorder='little')+hash_.to_bytes(length=16,byteorder='little')

def _makefileentry(start, end, hash_=0):
  return b""+start.to_bytes(length=8,byteorder='little')+end.to_bytes(length=8,byteorder='little')+hash_.to_bytes(length=8,byteorder='little')

file = open()

if nobootsector==True:
  file.seek(3) # skip past first 3 bytes
  file.write(b"KFS")
  file.write((2).to_bytes(length=2,byteorder='little')) # v2
  file.write((0).to_bytes(length=8,byteorder='little'))
else:
  file.write(boots)
file.seek(512*5) # skip past 5 sectors which can be any data
file.write(b"\0" * (512*1)) # 1 empty sector
dist = 512 # how many bytes are used to make it easy to truncate the sector
nexts = 12 # the next free sector
for i in files:
  file.write(_makedirfileentry(nexts)) # where the file entry is for that
  dist-=len(_makedirfileentry(nexts))
  nexts+=1
file.write(b'\0'*dist)

file.write(_makedirfileentry(11)) # give location of free sectors
file.write(b'\0'*1024-len(_makedirfileentry(11)))

