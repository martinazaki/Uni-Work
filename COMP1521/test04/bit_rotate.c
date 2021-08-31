#include "bit_rotate.h"

// return the value bits rotated left n_rotations
uint16_t bit_rotate(int n_rotations, uint16_t bits) {
    uint32_t bits_32 = bits;
    n_rotations = n_rotations %16;
    if (n_rotations < 0) {
        n_rotations += 16;
    } 

    bits_32 <<= n_rotations;
    return (bits_32 & 0xffff) | (bits_32 >> 16);
}
