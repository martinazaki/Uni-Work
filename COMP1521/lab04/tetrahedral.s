# Read a number n and print the first n tetrahedral numbers
# https://en.wikipedia.org/wiki/Tetrahedral_number

main:                  # int main(void) {

    la $a0, prompt     # printf("Enter how many: ");
    li $v0, 4
    syscall

    li $v0, 5           # scanf("%d", number);
    syscall
    move $t4, $v0

    li $t0, 1           # n = 1;

loop0:
    bgt $t0, $t4, end   # while (n <= how_many)
    li $t3, 0           # total = 0;
    li $t1, 0           # j = 1;

loop1:
    bgt $t1, $t0, print # while (j <= n)
    li $t2, 1           # i = 1;

loop2:
    bgt $t2, $t1, otherwise  # while (i <= j)
    add $t3, $t3, $t2   # total += i;
    add $t2, $t2, 1     # i++;
    b loop2

otherwise:        
    add $t1, $t1, 1     # j++;
    b loop1

print:    
    move $a0, $t3
    li   $v0, 1
    syscall

    li   $a0, '\n'      # printf("%c", '\n');
    li   $v0, 11
    syscall

    add $t0, $t0, 1     # n++;
    b loop0

end:
    jr   $ra            # return

    .data
prompt:
    .asciiz "Enter how many: "
