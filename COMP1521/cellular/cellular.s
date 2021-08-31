########################################################################
# COMP1521 20T2 --- assignment 1: a cellular automaton renderer
#
# Written by <<Martina Zaki>>, July 2020.


# Maximum and minimum values for the 3 parameters.

MIN_WORLD_SIZE	=    1
MAX_WORLD_SIZE	=  128
MIN_GENERATIONS	= -256
MAX_GENERATIONS	=  256
MIN_RULE	=    0
MAX_RULE	=  255

# Characters used to print alive/dead cells.

ALIVE_CHAR	= '#'
DEAD_CHAR	= '.'

# Maximum number of bytes needs to store all generations of cells.

MAX_CELLS_BYTES	= (MAX_GENERATIONS + 1) * MAX_WORLD_SIZE

	.data

# `cells' is used to store successive generations.  Each byte will be 1
# if the cell is alive in that generation, and 0 otherwise.

cells:	.space MAX_CELLS_BYTES


# Some strings you'll need to use:

prompt_world_size:	.asciiz "Enter world size: "
error_world_size:	.asciiz "Invalid world size\n"
prompt_rule:		.asciiz "Enter rule: "
error_rule:		.asciiz "Invalid rule\n"
prompt_n_generations:	.asciiz "Enter how many generations: "
error_n_generations:	.asciiz "Invalid number of generations\n"

	.text

	#
	# REPLACE THIS COMMENT WITH A LIST OF THE REGISTERS USED IN
	# `main', AND THE PURPOSES THEY ARE ARE USED FOR
	#
	# YOU SHOULD ALSO NOTE WHICH REGISTERS DO NOT HAVE THEIR
	# ORIGINAL VALUE WHEN `run_generation' FINISHES
	#

main:

	la	$a0, prompt_world_size		# printf("Enter world size: ");
	li	$v0, 4						
	syscall

	li	$v0, 5						# scanf("%d", &world_size);
	syscall
	move $s0, $v0					# world_size = 0

	bgt	$s0, 128, end0				# if(world_size > MAX_WORLD_SIZE) {
	blt $s0, 1, end0				# if(world_size < MIN_WORLD_SIZE)


	la	$a0, prompt_rule			# printf("Enter rule: ");
	li	$v0, 4						
	syscall

	li	$v0, 5						# scanf("%d", &rule);
	syscall
	move $s1, $v0					# rule = 0

	bgt	$s1, 255, end1				# if(rule > MAX_RULE) {
	blt $s1, 0, end1				# if(rule < MIN_RULE)


	la	$a0, prompt_n_generations	# printf("Enter how many generations: ");
	li	$v0, 4						
	syscall

	li   $a0, '\n'              	# printf("%c", '\n');
    li $v0, 11
    syscall

	li	$v0, 5						# scanf("%d", &n_generations);
	syscall
	move $s2, $v0					# n_generations = 0

	bgt	$s2, -256, end2				# if(n_generations > MAX_GENERATIONS) {
	blt $s2, 256, end2				# if(n_generations < MIN_GENERATIONS) {


	addi	$a0, $0, 0x0a			# putchar ('\n');
	addiu	$v0, $0, 11				# print_char
	syscall	

	li $s3, 0						# reverse = 0
	blt $s2, 0, end 				# if (n_generations < 0)
	li $s3, 1						# reverse = 1
	neg $s2, $s3					# n_generations = -n_generations

	# CELLS[0][WORLD_SIZE/2] = 1
	la  $t1, cells  				# t1 = &cells[0][0]
    li  $t3, 0      				# t3 = row = 0
    li  $t4, 0      				# t4 = col = 0

	#div $s0, 2						# world_size/2
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	li $t2, 1						# cells[...] = 1

	li $s4, 1						# g = 1

loop0:
	ble $s4, $s2, end				# while (g <= n_generations)
	jal run_generation				# run_generation
	add $s4, $s4, 1					# g++
	b loop0
	
	la $s3, loop2					# if (reverse), else loop2

loop1:
	move $s4, $s2					# g = n_generations
	bge $s4, 0, end					# g >= 0
	jal print_generation			# print_generation
	sub $s4, $s4, 1					# g--
	b loop1

loop2:
	li $s4, 0						# g = 0
	ble $s4, $s2, end				# while (g <= n_generations)
	jal print_generation			# print_generation
	add $s4, $s4, 1					# g++
	b loop2

end0:	
	la	$a0, error_world_size		# printf("Invalid world size\n");
	syscall

	jr	$ra							# return

end1:
	la	$a0, error_rule				# printf("Invalid rule\n");
	syscall

	jr	$ra							# return

end2:
	la	$a0, error_world_size		# printf("Invalid number of generations\n");
	syscall

	jr	$ra

done0:
	li  $v0, 0
	jr	$ra							# return 0


	#
	# Given `world_size', `which_generation', and `rule', calculate
	# a new generation according to `rule' and store it in `cells'.
	#

	#
	# REPLACE THIS COMMENT WITH A LIST OF THE REGISTERS USED IN
	# `run_generation', AND THE PURPOSES THEY ARE ARE USED FOR
	#
	# YOU SHOULD ALSO NOTE WHICH REGISTERS DO NOT HAVE THEIR
	# ORIGINAL VALUE WHEN `run_generation' FINISHES
	#

run_generation:

	li $s4, 0						# x = 0
	li $s7, 0						# which_generation = 0

loop3:
	blt $s4, $s0, done 				# while (x < world_size)

	li $s5, 0						# left = 0
	bgt $s4, 0, end					# if (x > 0)

	# cells[which_generation - 1][x - 1] = left
	la  $t1, cells  				# t1 = &cells[0][0]
    li  $t3, 0      				# t3 = row = 0
    li  $t4, 0      				# t4 = col = 0

	sub $t3, $s7, 1					# which_generation - 1
	sub $t4, $t4, 1					# x - 1
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	move $s5, $t2					# left = cells[which_generation - 1][x - 1]

	li $s6, 0						# centre = 0
	
	la  $t1, cells  				# t1 = &cells[0][0]

	sub $t3, $s7, 1					# which_generation - 1
	move $t4, $s4					# $t4 = x
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	move $s6, $t2					# centre = cells[which_generation - 1][x]


	li $s8, 0						# right = 0
	sub $s0, $s0, 1					# world_size = world_size - 1
	blt $s4, $s0, end				# if (x < world_size - 1)

	la  $t1, cells  				# t1 = &cells[0][0]

	sub $t3, $s7, 1					# which_generation - 1
	add $t4, $s4, 1					# $t4 = x + 1
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	move $s8, $t2					# right = cells[which_generation - 1][x + 1]

	sll $s5, $s5, 2					# left = left << 2
	sll $s6, $s6, 1					# centre = centre << 1
	sll $s8, $s8, 0					# right = right << 0

	or $t6, $s5, $s6				# $t6 = left | centre
	or $s9, $t6, $s8				# state = left | centre | right

	srl $t7, $s9, 1					# bit = 1 << state
	and $t8, $s1, $t7				# set = rule & bit

	la $t8, else					# if (set), else

	la  $t1, cells  				# t1 = &cells[0][0]

	move $t3, $s7					# which_generation
	move $t4, $s4					# $t4 = x
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	li $t2, 1						# cells = 1

	b loop3

else:

	la  $t1, cells  				# t1 = &cells[0][0]

	move $t3, $s7					# which_generation
	move $t4, $s4					# $t4 = x
	lw $t4, ($s0)					# load $s0 into reg $t4

    mul  $t0, $t3, $s1
    add  $t0, $t0, $t4
    add  $t5, $t0, $t1
    lb   $t2, ($t5)      			# load cell[row][col] into $t2

	li $t2, 0						# cells = 0

done1:
	li  $v0, 0
	jr	$ra							# return 0



	#
	# Given `world_size', and `which_generation', print out the
	# specified generation.
	#

	#
	# REPLACE THIS COMMENT WITH A LIST OF THE REGISTERS USED IN
	# `print_generation', AND THE PURPOSES THEY ARE ARE USED FOR
	#
	# YOU SHOULD ALSO NOTE WHICH REGISTERS DO NOT HAVE THEIR
	# ORIGINAL VALUE WHEN `print_generation' FINISHES
	#

print_generation:

	#move $a0, $s7               	# printf("%d", which_generation);
    #li  $v0, 1
    #syscall
	
	#addi	$a0, $0, 0x0a			# putchar ('\t');
	#addiu	$v0, $0, 11				# print_char
	#syscall	

#loop4:
	
	#blt $s4, $s0, end				# x < world_size

	
	jr	$ra
	
end:
