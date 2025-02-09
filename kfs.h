#ifndef __kfs_h
#define __kfs_h

// a struct for the table in the bootsector
struct kfs_bootsec {
  char code_[3]; // code jmp to code, nop
  char kfs[3]; // string "KFS"
  short ver; // uint16_t version = 2
  long long highlightedfile; // uint64_t sector of the file descriptor of a highlighted file
};

struct kfs_folder {
  char type;
  long long x;
  long long y;
  long long z;
};

struct kfs_folder1entry {
  char type; // uint8_t type=1
  unsigned long long back; // uint64_t previous sector
  unsigned long long next; // uint64_t next sector
  unsigned long long name; // uint64_t sector where the folders name is
};

struct kfs_folder2entry {
  char type; // uint8_t type=2
  unsigned long long sector; // uint64_t sector of file descriptor sector
  char hash[16]; // cityhash128 hash of file descriptor sector
};

struct kfs_folder3entry {
  char type; // uint8_t type=3
  unsigned long long sector; // uint64_t sector of first directory sector
  char hash[16]; // cityhash128 hash of first sector of directory
};

struct kfs_filenext {
  unsigned long long _; // uint64_t set to 0
  unsigned long long next; // uint64_t the next sector
  char hash[16]; // cityhash128 hash of the next sector
};

struct kfs_fileentry {
  unsigned long long start; // uint64_t start sector
  unsigned long long end; // uint64_t end sector
  char hash[16]; // cityhash128 hash of data
};

struct kfs_file {
  char name[40]; // string name
  unsigned long long creation; // uint64_t epoch creation
  unsigned long long lastmodification; // uint64_t epoch last modification
  unsigned long long lastread; // uint64_t epoch last read
  unsigned long long size; // uint64_t size in bytes
  unsigned char compression; // compression type
  unsigned char encryption; // encryption type
  struct kfs_fileentry entries[13];
};

// A dependencyless implementation of google's cityhash128. out is the uint128_t
void kfscityhash128(char *in, int size, char out[16]) {
  // todo lmao cityhash is pretty large :( 
}

#endif