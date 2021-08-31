#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "registers.h"

#define MAX_INSTRUCTION_CODES   1000

static int decode_instruction(uint32_t instruction, uint32_t *counter);
static void print_instruction(uint32_t instruction);

int main (int argc, char *argv[]) {
    char *temporary_directory;
    char temp[] = "/tmp/emu.XXXXXX";
    if ((temporary_directory = mkdtemp(temp)) == NULL) {
        fprintf(stderr,
                "%s: can not open create temporary directory: ", argv[0]);
        perror("");
        return 1;
    }
    
    FILE *f = fopen(argv[1], "r");
    
    int codes[MAX_INSTRUCTION_CODES];

    int i = 0;
    while (i < MAX_INSTRUCTION_CODES && fscanf(f, "%x", &codes[i]) == 1) {
        i++;
    }

    for (int j = 0; j < i; j++) {
        int decode_instruction();
    }
	
	fclose(f);
}

static int decode_instruction(uint32_t instruction, uint32_t *counter) {
    int reg0 = instruction >> 26;
    int reg1 = (instruction & 0x03e00000) >> 21;        // s and b
    int reg2 = (instruction & 0x001f0000) >> 16;        // t 
    int reg3 = (instruction & 0x0000f800) >> 11;        // d
    int reg4 = (instruction & 0x0000ffff);              // I and O 

    // The add Instruction
    if((instruction & 0xfc0007ff) == 0x00000020) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t sum = x + y;
        set_register(reg3, sum);

        (*counter) += reg3;
    }

    // The sub Instruction
    if((instruction & 0xfc0007ff) == 0x00000022) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t minus = x - y;
        set_register(reg3, minus);

        (*counter) += reg3;
    }

    // The mul Instruction
    if((instruction & 0xfc0007ff) == 0x70000002) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t mult = x * y;
        set_register(reg3, mult);

        (*counter) += reg3;
    }

    // The and Instruction
    if((instruction & 0xfc0007ff) == 0x00000024) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t andd = x & y;
        set_register(reg3, andd);

        (*counter) += reg3;
    }

    // The or Instruction
    if((instruction & 0xfc0007ff) == 0x00000025) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t orr = x | y;
        set_register(reg3, orr);

        (*counter) += reg3;
    }

    // The slt Instruction
    if((instruction & 0xfc0007ff) == 0x0000002A) {
        uint32_t x = get_register(reg1);
        uint32_t y = get_register(reg2);
        uint32_t less_than = x < y;
        set_register(reg3, less_than);

        (*counter) += 4;
    }

    // The addi Instruction
    if(reg0 == 8) {
        uint32_t x = get_register(reg1);
        uint32_t y = reg4;
        uint32_t add_imm = x + y;
        set_register(reg2, add_imm);

        (*counter) += 4;
    }

    // The andi Instruction
    if(reg0 == 12) {
        uint32_t x = get_register(reg1);
        uint32_t y = reg4;
        uint32_t and_imm = x & y;
        set_register(reg2, and_imm);

        (*counter) += 4;
    }
    
    // The ori Instruction
    if(reg0 == 13) {
        uint32_t x = get_register(reg1);
        uint32_t y = reg4;
        uint32_t or_imm = x | y;
        set_register(reg2, or_imm);

        (*counter) += 4;
    }

    // The slti Instruction
    if(reg0 == 10) {
        uint32_t x = get_register(reg1);
        uint32_t y = reg4;
        uint32_t less_imm = x < y;
        set_register(reg2, less_imm);

        (*counter) += 4;
    }

    // The lui Instruction
    if(reg0 == 15) {
        uint32_t x = reg4;
        uint32_t upper_imm = x << 16;
        set_register(reg2, upper_imm);

        (*counter) += 4;
    }

    // The beq Instruction
    if(reg0 == 4) {
        int PC = 0;
        (*counter) = PC;
        uint32_t x = get_register(reg2);
        uint32_t y = reg4;
        if(reg1 == x) {
            uint32_t branch_equal = y << 2;
            set_register(reg1, branch_equal);
            PC += branch_equal;
        } else {
            PC += 4;
        }
    }    

    // The bne Instruction
    if(reg0 == 5) {
        int PC = 0;
        (*counter) = PC;
        uint32_t x = get_register(reg2);
        uint32_t y = reg4;
        if(reg1 != x) {
            uint32_t branch_unequal = y << 2;
            set_register(reg1, branch_unequal);
            PC += branch_unequal;
        } else {
            PC += 4;
        }
    }     
    return 0;
}

static void print_instruction(uint32_t instruction) {
    int reg0 = instruction >> 26;
    int reg1 = (instruction & 0x03e00000) >> 21;        // s and b
    int reg2 = (instruction & 0x001f0000) >> 16;        // t 
    int reg3 = (instruction & 0x0000f800) >> 11;        // d
    int reg4 = (instruction & 0x0000ffff);              // I and O
    int reg6 = (instruction & 0x0000003f);              // x
    
    // The add Instruction
    if((instruction & 0xfc0007ff) == 0x00000020) {
        printf("add $%d, $%d, $%d", reg3, reg1, reg2);
    }

    // The sub Instruction
    if((instruction & 0xfc0007ff) == 0x00000022) {
        printf("sub $%d, $%d, $%d", reg3, reg1, reg2);
    }

    // The mul Instruction
    if((instruction & 0xfc0007ff) == 0x70000002) {
        printf("mul $%d, $%d, $%d", reg3, reg1, reg2);
    }

    // The and Instruction
    if((instruction & 0xfc0007ff) == 0x00000024) {
        printf("and $%d, $%d, $%d", reg3, reg1, reg2);
    }
    
    // The or Instruction 
    if((instruction & 0xfc0007ff) == 0x00000025) {
        printf("or $%d, $%d, $%d", reg3, reg1, reg2);
    }

    // The slt Instruction
    if((instruction & 0xfc0007ff) == 0x0000002A) {
        printf("slt $%d, $%d, $%d", reg3, reg1, reg2);
    }
    
    // The addi Instruction
    if(reg0 == 8) {
        printf("addi $%d, $%d, %d", reg2, reg1, (int16_t)reg4);
    }
    
    // The andi Instruction
    if(reg0 == 12) {
        printf("andi $%d, $%d, %d", reg2, reg1, reg4);
    }
    
    // The ori Instruction
    if(reg0 == 13) {
        printf("ori $%d, $%d, %d", reg2, reg1, reg4);
    }
    
    // The slti Instruction
    if(reg0 == 10) {
        printf("slti $%d, $%d, %d", reg2, reg1, reg4);
    }
    
    // The lui Instruction
    if(reg0 == 15) {
        printf("lui $%d, %d", reg2, reg4);
    }
    
    // The beq Instruction
    if(reg0 == 4) {
        printf("beq $%d, $%d, %d", reg1, reg2, reg4);
    }
    
    // The bne Instruction
    if(reg0 == 5) {
        printf("bne $%d, $%d, %d", reg1, reg2, reg4);
    }

    // The syscall Instruction
    if(reg6 == 12) {
        printf("syscall");
    }

}
