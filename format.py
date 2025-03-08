# utility for creating kfs2 discs.. until kfs.py is finished

# python format.py *name* *sizeinsectors* *bootsector file or 0* *files, first of which is highlighted*
# python format.py test.bin 128 kernel.abc
from sys import argv
import math
from io import TextIOWrapper
import os
import time

name = argv[1]
file = open(name, 'wb')
size = int(argv[2])
boots = argv[3]
nobootsector = True
if argv[3]!='0':
  boots=open(argv[3],'rb')
  nobootsector=False
files_ = []
files = []
try:
  files_= argv[4:]
except IndexError: pass # ignore
# 24576
sizeneeded = 11
for i in files_:
  i = open(i, 'rb')
  files.append(i)

def _makefileheader(name:bytes, size:int, creation=int(time.time()), modification=int(time.time()), lastread=int(time.time())) -> bytes:
  ret = b""
  ret += bytes(name,'ascii').ljust(40, b'\0') # name

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
  return b""+start.to_bytes(length=8,byteorder='little')+end.to_bytes(length=8,byteorder='little')+hash_.to_bytes(length=16,byteorder='little')

if nobootsector==True:
  file.seek(3) # skip past first 3 bytes
  file.write(b"KFS")
  file.write((2).to_bytes(length=2,byteorder='little')) # v2
  if len(files)>0:
    file.write((12).to_bytes(length=8,byteorder='little')) # first file will allways be at sector 12
  else:
    file.write((0).to_bytes(length=8,byteorder='little'))
else:
  file.write(boots.read())
file.seek(512*5) # skip past 5 sectors which can be any data
file.write(b"\0" * 512) # 1 empty sector
dist = 512 # how many bytes are used to make it easy to truncate the sector
nexts = 12 # the next free sector
for i in files:
  file.write(_makedirfileentry(nexts)) # where the file entry is for that
  dist-=len(_makedirfileentry(nexts))
  nexts += 1
  i.seek(0, os.SEEK_END) # set the cursor to the end to get file size
  nexts += math.ceil(i.tell()/512)
file.write(b'\0'*dist)

file.write(_makedirfileentry(11)) # give location of free sectors
file.write(b'\0'*(512-len(_makedirfileentry(11))))

file.write(b'\0'*1536) # skip 3 sectors

# garbage
# make the blank that tells what sectors are free
file.write(_makefileheader("",(size-(nexts-1))*512)) # how many sectors we used vs how much we were allocated
file.write(_makefileentry(nexts,size))
l = len(_makefileheader("",(size-(nexts-1))*512))+len(_makefileentry(nexts,size))
file.write(b'\0'*(512-l))

nexts = 12
dist = 0
while dist < len(files):
  files[dist].seek(0, os.SEEK_END)
  s = math.ceil(files[dist].tell()/512) # size in sectors
  h = _makefileheader(files_[dist],files[dist].tell())
  nexts+=1 # get past the header lol

  h += _makefileentry(nexts, nexts+s)
  file.write(h)
  file.write(b'\0'*(512-len(h))) # truncate

  files[dist].seek(0)
  data = files[dist].read()
  file.write(data) # write all data
  file.write(b'\0'*(512-(len(data)%512))) # truncate last sector
  
  files[dist].close()

  nexts += s
  dist+=1

file.write(b'\0'*(size-nexts))
file.close()