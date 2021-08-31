#  print the minimum of two integers
main:
    li $v0, 5           #   scanf("%d", &x);
    syscall             #
    move $a0, $v0

    li $v0, 5           #   scanf("%d", &y);
    syscall             #

    bge $v0, $a0, end   #   if (x < y)
    move $a0, $v0       #

end:
    li $v0, 1           #   printf("%d\n", 42);
    syscall
    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall

    li $v0, 0           # return 0
    jr $31
