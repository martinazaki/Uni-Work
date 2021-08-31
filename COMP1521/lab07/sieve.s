# Sieve of Eratosthenes
# https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
main:
    li $t0, 0           # i = 0
    
loop0:
    bge $t0, 1000, end0   # while (i < 1000) {
    
    la $t2, prime
    add $t3, $t2, $t0
    li $t4, 1
    sb $t4, ($t3)
    
    add $t0, $t0, 1

    b loop0             # }

end0:


    li $t0, 2          # i = 2

loop1:
    bge $t0, 1000, endif   # while (i < 1000) {

    la $t2, prime
    add $t3, $t2, $t0
    lb $t4, ($t3)
    bne $t4, 1, end1

    move $a0, $t0
    li $v0, 1
    syscall

    li $a0, '\n'
    li $v0, 11
    syscall

    mul $t1, $t0, 2

loop2:
    bge $t1, 1000, end1   # while (i < 1000) {

    la $t2, prime
    add $t3, $t2, $t1
    sb $0, ($t3)
    
    add $t1, $t1, $t0
    b loop2             # }

end1:
    add $t0, $t0, 1
    b loop1

endif:
    li $v0, 0
    jr $31

.data
prime:
    .space 1000