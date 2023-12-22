# kfs utility
from io import FileIO

class kfs:
  root = b"" # first folder "/"
  garbagebin = b"" # garbage bin
  
  def _getsector(self, sector):
    self.file.seek((sector-1)*512)
    return self.file.read(512)

  def _makefileheader(self, name, creation, modification, lastread, size) -> bytes:
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
    pass

  def close(self):
    self.file.close()

  def getinfo(self, path:str) -> dict:
    pass

  def getdata(self, path:str) -> str:
    pass

if __name__ == "__main__":
  from sys import argv