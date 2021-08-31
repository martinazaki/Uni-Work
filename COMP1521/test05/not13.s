main:
    li $v0, 5           #   scanf("%d", &x);
    syscall             #
    move $t0, $v0

    li $v0, 5           #   scanf("%d", &y);
    syscall             #
    move $t1, $v0

    add $t2, $t0, 1     #   i = x + 1;

loop0:
    bge $t2, $t1, end0  #   while (i < y)    
    beq $t2, 13, next   #   if (i != 13)
    move $a0, $t2

    li $v0, 1           #   printf("%d\n", 42);
    syscall

    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall

next:
    add $t2, $t2, 1     #   i++;
    b loop0

end0:
    li $v0, 0           # return 0
    jr $31
