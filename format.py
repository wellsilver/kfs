# utility for creating kfs2 discs.. until kfs.py is finished

# python format.py *name* *sizeinsectors* *files, first of which is highlighted*
# python format.py test.bin 128 kernel.abc
from sys import argv
import time

name = argv[3]
size = int(argv[4])

files_, files = []
try:
  files_= argv[6:]
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

file.seek(3) # skip past first 3 bytes
file.write(b"KFS")
file.write((2).to_bytes(length=2,byteorder='little')) # v2
file.write((0).to_bytes(length=8,byteorder='little'))
file.seek(512*5) # skip past 5 sectors which can be any data
file.write(b"\0" * (512*1)) # 1 empty sector
nexts = 12
for i in files:
  file.write(_makedirfileentry(nexts)) # where the file entry is for that
  nexts+=1

file.write(_makedirfileentry(11).ljust(512,b'\0')) # make file
file.write(b"\0" * 512)
file.write(_makefileheader(b"", size-(512*11)))