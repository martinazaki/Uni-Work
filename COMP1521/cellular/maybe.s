
		#####
	#TO DO :PUTCHAR('\n');

	blt	$t2, 0, reverse_end			# if(n_generations < 0) {

		#####
	#cells[0][world_size / 2] = 1;
	mul $t3, $t0, 24				# cells[0][world_size / 2] = 1;
	add $t4, $t3, 0
	mul $t5, $t4, 4
	la $t6, array
	add $t7, $t6, $t5

loop0:
	li	$t8, 1						# g = 1;

	bge	$t2, $t8, run_generation	# run_generation(world_size, g, rule);
	
	add $t8, $t8, 1					# g++;

	b loop0

	######
	#if reverse

loop1:
	li $t8, run_generation			# g = n_generations;
	
	bge $t8, 0, print_generation	# print_generation(world_size, g);

	sub $t8, $t8, 1					# g--;

	b loop1

loop2:
	li $t8, 0						# g = n_generations;
	
	bge 0, $t8, print_generation	# print_generation(world_size, g);

	add $t8, $t8, 1					# g++;

	b loop2


reverse_end:
	li	$t8, 1						# reverse = 1

		#####
	#sw $t2, -($t2)		STUPID			# n_generations = -n_generations

    
