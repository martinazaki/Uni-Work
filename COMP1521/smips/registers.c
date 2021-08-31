#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "registers.h"

const char *const map_name[] = {
    [zero] = "$zero", [at] = "$at", [v0] = "$v0", [v1] = "$v1", [a0] = "$a0",
    [a1] = "$a1",     [a2] = "$a2", [a3] = "$a3", [t0] = "$t0", [t1] = "$t1",
    [t2] = "$t2",     [t3] = "$t3", [t4] = "$t4", [t5] = "$t5", [t6] = "$t6",
    [t7] = "$t7",     [s0] = "$s0", [s1] = "$s1", [s2] = "$s2", [s3] = "$s3",
    [s4] = "$s4",     [s5] = "$s5", [s6] = "$s6", [s7] = "$s7", [t8] = "$t8",
    [t9] = "$t9",     [k0] = "$k0", [k1] = "$k1", [gp] = "$gp", [sp] = "$sp",
    [fp] = "$fp",     [ra] = "$ra",
};

static uint32_t registers[N_REGISTERS] = { 0 };

uint32_t get_register(regtype number) {
    assert(number >= 0 && number < N_REGISTERS);
    return registers[number];
}

void set_register(regtype number, uint32_t value) {
    assert(number >= 0 && number < N_REGISTERS);
    if (number != zero) {
        registers[number] = value;
    }
}
