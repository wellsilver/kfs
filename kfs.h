// too lazy to write this, will just make the structures
#include <stdint.h>

enum kfs_fse_types {
  // undefined rn
  kfs_empty = 0,
  kfs_blankextender = 254
};

struct kfs_fs_extender {
  uint8_t type; // kfs_fse_types enum
  uint64_t start;
  uint64_t end;
  uint8_t data[47]; // any
};

enum kfs_folderentry {
  kfs_descriptor = 1,
  kfs_filedesc = 2,
  kfs_filedata = 3,
  kfs_folder = 4
};

struct kfs_folderentry_descriptor {
  uint8_t type; // kfs_folderentry enum
  uint64_t previous;
  uint64_t next;
  uint8_t blank[15]; // any
};

struct kfs_folderentry_filedata {
  uint8_t type;// kfs_folderentry enum
  uint64_t first;
  uint64_t last;
  uint16_t id;
  uint64_t distance;
  uint8_t blank[5];
};

struct kfs_folderentry_file {
  uint8_t type; // kfs_folderentry enum
  uint16_t id;
  uint8_t encryptionmethod;
  uint8_t compressionmethod;
  uint64_t creationdate;
  uint64_t modificationdate;
  uint8_t blank[10];
};