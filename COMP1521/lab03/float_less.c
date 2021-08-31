// Compare 2 floats using bit operations only

#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "floats.h"

// float_less is given the bits of 2 floats bits1, bits2 as a uint32_t
// and returns 1 if bits1 < bits2, 0 otherwise
// 0 is return if bits1 or bits2 is Nan
// only bit operations and integer comparisons are used
uint32_t float_less(uint32_t bits1, uint32_t bits2) {
	if (((bits1 >> 23) & 255) == 255 && (bits1 & 8388607) != 0) {
		return 0;
    }  

	if (((bits2 >> 23) & 255) == 255 && (bits2 & 8388607) != 0) {
		return 0;
    }    
	
	int m = (bits1 >> 31);
	int n = (bits2 >> 31);
	if (m == 1 && n == 0)
		return 1;
	if (m == 0 && n == 1)
		return 0;

	int a = ((bits1 >> 23) & 255);
	int b = ((bits2 >> 23) & 255);
	if (a < b) {
		return m == 0;
    }    
	else if (a > b) {
		return m == 1;
    }     
	else {
		int e = (bits1 & 8388607);
		int f = (bits2 & 8388607);
		if ((e < f && m == 0) || (e > f && m == 1))
			return 1;
		else
			return 0;
	}
}
