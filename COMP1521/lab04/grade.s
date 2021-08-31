# read a mark and print the corresponding UNSW grade

main:
    la $a0, prompt      # printf("Enter a mark: ");
    li $v0, 4
    syscall

    li $v0, 5           # scanf("%d", mark);
    syscall

    li $t0, 50          # if (x < 50);
    blt $v0, $t0, fail

    li $t1, 65          # if (x < 65);
    blt $v0, $t1, pass

    li $t2, 75          # if (x < 75);
    blt $v0, $t2, credit

    li $t3, 85          # if (x < 85);
    blt $v0, $t3, distinction

    la $a0, hd          # printf("HD\n");
    li $v0, 4     
    syscall

    j end
    
fail:

    la $a0, fl          # printf("FL\n");
    li $v0, 4
    syscall

    j end

pass:
    la $a0, ps          # printf("PS\n");
    li $v0, 4
    syscall

    j end

credit:
    la $a0, cr          # printf("CR\n");
    li $v0, 4
    syscall

    j end

distinction:

    la $a0, dn          # printf("DN\n");
    li $v0, 4
    syscall

end:

    jr $ra              # return

    .data

prompt:
    .asciiz "Enter a mark: "
fl:
    .asciiz "FL\n"
ps:
    .asciiz "PS\n"
cr:
    .asciiz "CR\n"
dn:
    .asciiz "DN\n"
hd:
    .asciiz "HD\n"
