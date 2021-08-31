// Sample solution for COMP1521 lab exercises
//
// generate the opcode for an addi instruction

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "addi.h"

// return the MIPS opcode for addi $t,$s, i
uint32_t addi(int t, int s, int i) {

    uint32_t opcode = 0x20000000; 
    uint16_t imm = i;
    
    opcode = opcode | (s << 21);
    opcode = opcode | (t << 16); 
    opcode = opcode | imm;
    
    return opcode;

}
