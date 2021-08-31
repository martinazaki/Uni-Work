main:
    li $v0, 5           #   scanf("%d", &x);
    syscall             #
    move $t0, $v0

    li $t1, 0           #   i = 0;

loop0:
    bge $t1, $t0, end0  #   while (i < x)
    
    li $t2, 0           # j = 0

loop1:
    bge $t2, $t0, end1  #   while (j < x) 

    li $a0, '*'         #   printf("%c\n", '*');
    li $v0, 11
    syscall

    add $t2, $t2, 1     #   j++;

    b loop1

end1:
    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall
    
    add $t1, $t1, 1     #   i++;

    b loop0

end0:
    li $v0, 0           # return 0
    jr $31
