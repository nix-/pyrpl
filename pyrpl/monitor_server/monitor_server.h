#pragma once

#include <limits.h>


#define FATAL                                                                  \
    do {                                                                       \
        fprintf(stderr, "Error at line %d, file %s (%d) [%s]\n", __LINE__,     \
                __FILE__, errno, strerror(errno));                             \
        error("FATAL ERROR");                                                  \
        exit(1);                                                               \
    } while (0)


#define MAP_SIZE 131072UL
//allowed address space: 0x40000000 to 0x40800000 has size 0x800000 = 128*65536 = 8388608
#define MAP_MASK (MAP_SIZE - 1)
#define MAX_LENGTH USHRT_MAX // 65535
