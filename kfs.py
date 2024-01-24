# kfs utility
from io import FileIO
import time
import struct
import os

class kfs:
  root = b"" # first folder "/"
  garbagebin = b"" # garbage bin
  
  def _getsector(self, sector):
    self.file.seek((sector-1)*512)
    return self.file.read(512)

  def _writesector(self, sector, data):
    self.file.seek((sector-1)*512)
    return self.file.write(data)

  def _makefileheader(self, name:bytes, size:int, creation=int(time.time()), modification=int(time.time()), lastread=int(time.time())) -> bytes:
    ret = b""
    ret += name.ljust(40, b'\0') # name

    ret += creation.to_bytes(length=8,byteorder='little') # epoch creation
    ret += modification.to_bytes(length=8,byteorder='little') # epoch last modification
    ret += lastread.to_bytes(length=8,byteorder='little') # epoch last read
    ret += size.to_bytes(length=8,byteorder='little') # size in bytes

    ret += (0).to_bytes(byteorder='little')
    ret += (0).to_bytes(byteorder='little')
    return ret

  def _makedirfileentry(self, pos:int, hash_=0):
    return b""+(2).to_bytes(byteorder='little')+pos.to_bytes(length=8,byteorder='little')+hash_.to_bytes(length=16,byteorder='little')

  def _makefileentry(self, start, end, hash_=0):
    return b""+start.to_bytes(length=8,byteorder='little')+end.to_bytes(length=8,byteorder='little')+hash_.to_bytes(length=8,byteorder='little')
  
  def _dirfindtype(self, data, type_:int):
    loop=0
    while loop<len(data): # loop through directory entries to look for type
      data = struct.unpack("B Q Q Q", data[loop:loop+(1+8+16)]) # get entry

      if data[0] == type_: return data
      loop+=(1+8+16) # loop
    return None
      
  def __init__(self, file:FileIO):
    self.file = file

    self.file.seek(0, os.SEEK_END)
    size = self.file.tell()
    if size < 512*11: # 11 sectors are required
      raise OverflowError("11 sectors (11*512 bytes) space required for kfs")

    self.root = self._getsector(7)
    self.garbagebin = self._getsector(8)

  def format(self):
    self.file.seek(0, os.SEEK_END)
    size = self.file.tell()
    if size < 512*11: # 11 sectors are required
      raise OverflowError("11 sectors (11*512 bytes) space required for kfs")
    self.file.seek(0)
    self.file.seek(3) # skip past first 3 bytes
    self.file.write(b"KFS")
    self.file.write((2).to_bytes(length=2,byteorder='little')) # v2
    self.file.write((0).to_bytes(length=8,byteorder='little'))
    self.file.seek(512*5) # skip past 5 sectors which can be any data
    self.file.write(b"\0" * (512*2)) # 2 empty sectors
    if size > 512*11: # add a file to garbage bin with free area
      self.file.write(self._makedirfileentry(11).ljust(512,b'\0')) # make file
      self.file.write(b"\0" * 512)
      self.file.write(self._makefileheader(b"", size-(512*11)))
      self.file.write(self._makefileentry(12, (size-(512*11))/512)) # add free space to file
    else:
      self.file.write(b"\0" * (512*2))
    
  def close(self):
    self.file.close()

  # get info on a file
  def getinfo(self, path:str) -> dict:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)

  # get data on a file
  def getdata(self, path:str) -> str:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)

  def getdir(self, path:str) -> dict[str]:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)

  def replacefile(self, path:str, data) -> None:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)
  
  def makefile(self, path:str, data) -> None:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)
    
  def makedir(self, path:str) -> None:
    path:dict = path.split("/")
    if path[0] == '': path.pop(0)
    if path[-1] == '': path.pop(-1)
    name = path[-1];path.pop(-1) # save the new folders name
    currentdir = 7
    
    # get to the sector that contains the folder
    for i in path:
      d = self._getsector(currentdir)
      e = self._dirfindtype(d,3)
      while e!=None:
        t = self._getsector(e[1])
        t = self._dirfindtype(t, 1)
        if self._getsector(t[3]) == i:
          currentdir = e[1]
          break

        e=self._dirfindtype(d,3)
    
    d = self._getsector(currentdir)
    # find a free space
    loop=0
    while loop<len(data): # loop through directory entries to look for type
      data = struct.unpack("B Q Q Q", data[loop:loop+(1+8+16)]) # get entry

      if data[0] == 0: return data
      loop+=(1+8+16) # loop
    # free space is at loop
    data[loop:loop] = (3).to_bytes(byteorder='little')
    data[loop+1:loop+1+8] = (0).to_bytes(byteorder='little') # sector here
    data[loop+1+8:loop+1+8+16] = (0).to_bytes(length=16)

    self._writesector(currentdir, data)
    


# to make a kfs file:
# python kfs.py -f out.kfs -c -add filename1 -add filename2

if __name__ == "__main__":
  from sys import argv
  dist = 0

  file = ""
  format_ = False
  size = 512*11
  access = 'br'
  add = []
  extract = []
  try:
    while dist < len(argv):
      i = argv[dist];dist+=1

      if i == "-f" or i == "--file": # select file
        i = argv[dist];dist+=1
        file = i
      if i == "-w": # allow writing
        access = 'ba+'
      if i == "-r": # only allow reading
        access = 'br'
      if i == "-x": # extract this file with its data (to the current directory)
        i = argv[dist];dist+=1
        extract.append()
      if i == "-s": # when creating a file truncate to size
        i = argv[dist];dist+=1
        if i.lower().endswith("k"): # kilobytes
          i[-1] = ''
          size = int(i)*pow(2,10)
        elif i.lower().endswith("m"): # megabytes
          i[-1] = ''
          size = int(i)*pow(2,20)
        elif i.lower().endswith("g"): # gigabytes
          i[-1] = ''
          size = int(i)*pow(2,30)
        else:
          size = int(i)
        
      if i == "-c": # create a new file
        format_ = True
      if i == '-a' or i == "--add": # add a file
        i = argv[dist];dist+=1
        try:
          add.append(open(i,'r'))
        except:
          print("File \""+i+"\" Not accessible")
          quit(-2)

  except IndexError:
    print("Invalid \""+i+"\"")
    quit(-1)
  
  if format_: 
    access = "bx"
    try:
      f = open(file,'bx+')
    except:
      print("Cant make "+file);quit(-3)
    f.truncate(size)
  else:
    try: f = open(file,access)
    except: print("Cant open "+file);quit(-3)

  main=kfs(f)

  if format_:
    main.format()

  

  main.close()