# read a line and print its length

main:
    la   $a0, str0       # printf("Enter a line of input: ");
    li   $v0, 4
    syscall

    la   $a0, line
    la   $a1, 256
    li   $v0, 8          # fgets(buffer, 256, stdin)
    syscall              #

    li $t0, 0
    move $t1, $a0

    mul $t2, $t0, 1
    add $t2, $t2, $t1
    lb $t3, ($t2)

loop0:
    beq $t3, 0, end

    add $t0, $t0, 1

    mul $t2, $t0, 1
    add $t2, $t2, $t1
    lb $t3, ($t2)

    j loop0

end:        
    la   $a0, str1       # printf("Line length: ");
    li   $v0, 4
    syscall

    move   $a0, $t0         # printf("%d", i);
    li   $v0, 1
    syscall

    li   $a0, '\n'       # printf("%c", '\n');
    li   $v0, 11
    syscall

    li   $v0, 0          # return 0
    jr   $31


.data
str0:
    .asciiz "Enter a line of input: "
str1:
    .asciiz "Line length: "


# line of input stored here
line:
    .space 256

