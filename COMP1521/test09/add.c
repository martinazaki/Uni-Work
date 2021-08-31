#include <stdio.h>
#include <stdint.h>
#include <assert.h>

#include "add.h"

// return the MIPS opcode for add $d, $s, $t
uint32_t add(uint32_t d, uint32_t s, uint32_t t) {

    assert(0 <= d && d < 32);
    assert(0 <= s && s < 32);
    assert(0 <= t && t < 32);

    return s << 21 |
           t << 16 |
           d << 11 |
           0x20;

}
