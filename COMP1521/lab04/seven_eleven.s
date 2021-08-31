# Read a number and print positive multiples of 7 or 11 < n

main:                           # int main(void) {

    la $a0, prompt              # printf("Enter a number: ");
    li $v0, 4
    syscall

    li $v0, 5                   # scanf("%d", number);
    syscall
    move $t0, $v0
    
    li    $t1, 1                # i = 1;


loop0:                          # loop:
    bge  $t1, $t0, end          # if (number < i) goto end;
    
    rem $v0, $t1, 7             # i divided by 7
    beq $v0, 0, print           # if mod == 0, jump over to Lmod and increment

    rem $v0, $t1, 11            # i divided by 11
    bne $v0, 0, Lmod            # if mod == 0, jump over to Lmod and increment

print:
    move $a0, $t1               # printf("%d" i);
    li   $v0, 1
    syscall
    
    li   $a0, '\n'              # printf("%c", '\n');
    li $v0, 11
    syscall

Lmod:   
    add $t1, $t1, 1             # i++
    j loop0                     # repeat the while loop
    
end:
    jr   $ra           # return

    .data

prompt:
    .asciiz "Enter a number: "
