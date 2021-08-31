#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

int bcd(int bcd_value);

int main(int argc, char *argv[]) {

    for (int arg = 1; arg < argc; arg++) {
        long l = strtol(argv[arg], NULL, 0);
        assert(l >= 0 && l <= 0x0909);
        int bcd_value = l;

        printf("%d\n", bcd(bcd_value));
    }

    return 0;
}

// given a  BCD encoded value between 0 .. 99
// return corresponding integer
int bcd(int bcd_value) {

    int ans1 = 0;
    int ans2 = 0;
    
    int i = 0;
    while (i < 8) {
        unsigned int mask = 1 << (16 - 1 - i);

        if (bcd_value & mask) {
            ans1 |= mask;

        }
        i++;
    }
    ans1 >>= 8;

    while (i < 16) {
        unsigned int mask = 1 << (16 - 1 - i);

        if (bcd_value & mask) {
            ans2 |= mask;

        }
        i++;

    }
    return ans1*10 + ans2;
}

