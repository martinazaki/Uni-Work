// swap pairs of bits of a 64-bit value, using bitwise operators

#include <assert.h>
#include <stdint.h>
#include <stdlib.h>

// return value with pairs of bits swapped
uint64_t bit_swap(uint64_t value) {
    value = ((value & 0x00000000000000FFULL) << 56) |
             ((value & 0x000000000000FF00ULL) << 40) |
             ((value & 0x0000000000FF0000ULL) << 24) |
             ((value & 0x00000000FF000000ULL) << 8) |
             ((value & 0x000000FF00000000ULL) << 8) |
             ((value & 0x0000FF0000000000ULL) << 24) |
             ((value & 0x00FF000000000000ULL) << 40) |
             ((value & 0xFF00000000000000ULL) << 56);

    return value;
}
