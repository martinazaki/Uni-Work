# read a line and print whether it is a palindrom

main:
    la   $a0, str0       # printf("Enter a line of input: ");
    li   $v0, 4
    syscall

    la   $a0, line
    la   $a1, 256
    li   $v0, 8          # fgets(buffer, 256, stdin)
    syscall              #

    li $t0, 0            # i = 0

loop0:
    la $t3, line
    add $t4, $t3, $t0
    lb $t5, ($t4)
    beq $t5, 0, end0

    addi $t0, $t0, 1
    b loop0

end0:


    li $t1, 0       
    add $t2, $t0, -2

loop1:
    bge $t1, $t2, end1

    la $t3, line
    add $t4, $t3, $t1
    lb $t5, ($t4)
    add $t6, $t3, $t2
    lb $t7, ($t6)

    beq $t5, $t7, same
    la $a0, not_palindrome

    b done

same:
    addi $t1, $t1, 1
    addi $t2, $t2, -1
    b loop1

end1:

    la $a0, palindrome

done:   
    li $v0, 4
    syscall

    li $v0, 0
    jr $31


.data
str0:
    .asciiz "Enter a line of input: "
palindrome:
    .asciiz "palindrome\n"
not_palindrome:
    .asciiz "not palindrome\n"


# line of input stored here
line:
    .space 256

