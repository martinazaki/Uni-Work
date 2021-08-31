// Multiply a float by 2048 using bit operations only

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "floats.h"

// float_2048 is given the bits of a float f as a uint32_t
// it uses bit operations and + to calculate f * 2048
// and returns the bits of this value as a uint32_t
//
// if the result is too large to be represented as a float +inf or -inf is returned
//
// if f is +0, -0, +inf or -int, or Nan it is returned unchanged
//
// float_2048 assumes f is not a denormal number
//
uint32_t float_2048(uint32_t f) {
    if (((f >> 23) & 255) == 255 && (f & (1 << 23)) != 0)
		return f;
	if ((f & 2147483647) == 0)
		return f;
	
	uint32_t a = 1;
	if (((f >> 23) & 255) + 11 > 255) {
		//a = (f | (1 << 31));
		//a -= (a & (1 << 23));
		a = (255 << 23) + ((f >> 31) << 31);
	}
	else
		a = f + (11 << 23);
	return a;
}
