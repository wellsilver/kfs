# kfs utility
from io import FileIO
import os

class kfs:
  root = b"" # first folder "/"
  garbagebin = b"" # garbage bin
  
  def _getsector(self, sector):
    self.file.seek((sector-1)*512)
    return self.file.read(512)

  def _makefileheader(self, name, creation, modification, lastread, size) -> bytes:
    pass

  def _makefileentry(self):
    pass
  
  def __init__(self, file:FileIO, createifinvalid=True):
    self.file = file
    self.file.seek(3)
    if self.file.read(3) != "kfs" and not createifinvalid:
      raise ValueError("Not a kfs file")
    elif self.file.read(3) != "kfs":
      self.format()
    
    root = bytes(self._getsector(7))
    garbagebin = bytes(self._getsector(8))

  def format(self):
    self.file.seek(0, os.SEEK_END)
    size = self.file.tell()
    if size < 512*10: # 10 sectors are required
      raise OverflowError("10 sectors (10*512 bytes) space required for kfs")
    self.file.seek(0)
    self.file.seek(3) # skip past first 3 bytes
    self.file.write(b"KFS")
    self.file.write((2).to_bytes(length=2,byteorder='little')) # v2
    self.file.write((0).to_bytes(length=8,byteorder='little'))
    self.file.seek(512*5) # skip past 5 sectors which can be any data
    self.file.write(b"" * (512*2)) # 2 empty sectors
    

  
  def close(self):
    self.file.close()

  def getinfo(self, path:str) -> dict:
    pass

  def getdata(self, path:str) -> str:
    pass

if __name__ == "__main__":
  from sys import argv