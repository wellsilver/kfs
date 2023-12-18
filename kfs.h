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
  struct {
    char type;
    long long x;
    long long y;
    long long z;
  } entries; // blank. this is a table, all entrys are this size however.
};

struct kfs_folder1entry {
  char type; // uint8_t type=1
  long long back; // uint64_t previous sector
  long long next; // uint64_t next sector
  long long name; // uint64_t sector where the folders name is
};

struct kfs_folder2entry {
  char type; // uint8_t type=2
  long long sector; // uint64_t sector of file descriptor sector
  char hash[16]; // cityhash128 hash of file descriptor sector
};

struct kfs_folder3entry {
  char type; // uint8_t type=3
  long long sector; // uint64_t sector of first directory sector
  char hash[16]; // cityhash128 hash of first sector of directory
};

struct kfs_file {
  char name[40]; // string name
  long long creation; // uint64_t epoch creation
  long long lastmodification; // uint64_t epoch last modification
  long long lastread; // uint64_t epoch last read
  long long size; // uint64_t size in bytes
  char compression; // compression type
  char encryption; // encryption type
  struct kfs_fileentry entries[13];
};

struct kfs_filenext {
  long long blank;
  long long next;
  char hash[16];
};

struct kfs_fileentry {
  long long start;
  long long end;
  char hash[16];
};

// A dependencyless implementation of google's cityhash128. out is the uint128_t
void kfscityhash128(char *in, int size, char out[16]) {
  
}

#endif