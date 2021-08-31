#include <stdio.h>
#include <stdint.h>
#include "smips.h"

void print_instruction(uint32_t instruction) {
//    int ref0 = instruction >> 26;
    int ref1 = (instruction & 0x03e00000) >> 21;        // s and b
    int ref2 = (instruction & 0x001f0000) >> 16;        // t 
    int ref3 = (instruction & 0x0000f800) >> 11;        // d
//    int ref4 = (instruction & 0x0000ffff);              // I and O 
//    int ref5 = (instruction & 0x000007c0) >> 6;         // new I
//    int ref6 = (instruction & 0x0000003f);              // x
//    int last_16 = (instruction & 0x0000ffff);

    // The add Instruction
    if((instruction & 0xfc0007ff) == 0x00000020) {
        printf("add $%d, $%d, $%d", ref3, ref1, ref2);
        // uint32_t x = get_register(ref1);
        // uint32_t y = get_register(ref2);
        // uint32_t sum = x + y;
        // set_register(ref3, sum);

        // (*program_counter) += ref3;
    }

    // // The sub Instruction
    // if((instruction & 0xfc0007ff) == 0x00000022) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = get_register(ref2);
    //     uint32_t minus = x - y;
    //     set_register(ref3, minus);

    //     (*program_counter) += ref3;
    // }

    // // The mul Instruction
    // if((instruction & 0xfc0007ff) == 0x70000002) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = get_register(ref2);
    //     uint32_t mult = x * y;
    //     set_register(ref3, mult);

    //     (*program_counter) += ref3;
    // }

    // // The and Instruction
    // if((instruction & 0xfc0007ff) == 0x00000024) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = get_register(ref2);
    //     uint32_t andd = x & y;
    //     set_register(ref3, andd);

    //     (*program_counter) += ref3;
    // }

    // // The or Instruction
    // if((instruction & 0xfc0007ff) == 0x00000025) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = get_register(ref2);
    //     uint32_t orr = x | y;
    //     set_register(ref3, orr);

    //     (*program_counter) += ref3;
    // }

    // // The slt Instruction
    // if((instruction & 0xfc0007ff) == 0x0000002A) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = get_register(ref2);
    //     uint32_t less_than = x < y;
    //     set_register(ref3, less_than);

    //     (*program_counter) += 4;
    // }

    // // The addi Instruction
    // if(ref0 == 8) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = ref4;
    //     uint32_t add_imm = x + y;
    //     set_register(ref2, add_imm);

    //     (*program_counter) += 4;
    // }

    // // The andi Instruction
    // if(ref0 == 12) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = ref4;
    //     uint32_t and_imm = x & y;
    //     set_register(ref2, and_imm);

    //     (*program_counter) += 4;
    // }
    
    // // The ori Instruction
    // if(ref0 == 13) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = ref4;
    //     uint32_t or_imm = x | y;
    //     set_register(ref2, or_imm);

    //     (*program_counter) += 4;
    // }

    // // The slti Instruction
    // if(ref0 == 10) {
    //     uint32_t x = get_register(ref1);
    //     uint32_t y = ref4;
    //     uint32_t less_imm = x < y;
    //     set_register(ref2, less_imm);

    //     (*program_counter) += 4;
    // }

    // // The lui Instruction
    // if(ref0 == 15) {
    //     uint32_t x = ref4;
    //     uint32_t upper_imm = x << 16;
    //     set_register(ref2, upper_imm);

    //     (*program_counter) += 4;
    // }

    // // The beq Instruction
    // if(ref0 == 4) {
    //     int PC = 0;
    //     (*program_counter) = PC;
    //     uint32_t x = get_register(ref2);
    //     uint32_t y = ref4;
    //     if(ref1 == x) {
    //         uint32_t branch_equal = y << 2;
    //         set_register(ref1, branch_equal);
    //         PC += branch_equal;
    //     } else {
    //         PC += 4;
    //     }
    // }    

    // // The bne Instruction
    // if(ref0 == 5) {
    //     int PC = 0;
    //     (*program_counter) = PC;
    //     uint32_t x = get_register(ref2);
    //     uint32_t y = ref4;
    //     if(ref1 != x) {
    //         uint32_t branch_unequal = y << 2;
    //         set_register(ref1, branch_unequal);
    //         PC += branch_unequal;
    //     } else {
    //         PC += 4;
    //     }
    // }     

}    