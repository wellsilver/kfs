# kfs utility
from io import FileIO
import time
import os

class kfs:
  root = b"" # first folder "/"
  garbagebin = b"" # garbage bin
  
  def _getsector(self, sector):
    self.file.seek((sector-1)*512)
    return self.file.read(512)

  def _makefileheader(self, name:str, size:int, creation=int(time.time()), modification=int(time.time()), lastread=int(time.time())) -> bytes:
    ret = b""
    ret += name.ljust(40, '\0') # name

    ret += creation.to_bytes(length=8,byteorder='little') # epoch creation
    ret += modification.to_bytes(length=8,byteorder='little') # epoch last modification
    ret += lastread.to_bytes(length=8,byteorder='little') # epoch last read
    ret += size.to_bytes(length=8,byteorder='little') # size in bytes

    ret += (0).to_bytes(byteorder='little')
    ret += (0).to_bytes(byteorder='little')
    return ret

  def _makedirfileentry(self, pos:int, hash=0):
    return b""+(2).to_bytes(byteorder='little')+pos.to_bytes(length=8,byteorder='little')+hash.to_bytes(length=16,byteorder='little')

  def _makefileentry(self, start, end):
    pass
  
  def __init__(self, file:FileIO):
    self.file = file

    size = self.file.tell()
    if size < 512*11: # 11 sectors are required
      raise OverflowError("11 sectors (11*512 bytes) space required for kfs")

    self.root = bytes(self._getsector(7))
    self.garbagebin = bytes(self._getsector(8))

  def format(self):
    self.file.seek(0, os.SEEK_END)
    size = self.file.tell()
    if size < 512*11: # 11 sectors are required
      raise OverflowError("11 sectors (11*512 bytes) space required for kfs")
    self.file.seek(3) # skip past first 3 bytes
    self.file.write(b"KFS")
    self.file.write((2).to_bytes(length=2,byteorder='little')) # v2
    self.file.write((0).to_bytes(length=8,byteorder='little'))
    self.file.seek(512*5) # skip past 5 sectors which can be any data
    self.file.write(b"\0" * (512*2)) # 2 empty sectors
    if size > 512*11: # add a file to garbage bin with free area
      self.file.write(self._makedirfileentry(11).ljust(512,b'\0')) # make file
      self.file.write(b"\0" * 512)
      self.file.write(self._makefileheader("", size-(512*11)))
      self.file.write(self._makefileentry(12, size-(512*11))) 
    else:
      self.file.write(b"\0" * (512*2))
    
  def close(self):
    self.file.close()

  def getinfo(self, path:str) -> dict:
    pass

  def getdata(self, path:str) -> str:
    pass

if __name__ == "__main__":
  from sys import argv