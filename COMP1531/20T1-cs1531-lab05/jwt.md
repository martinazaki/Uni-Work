## Part 1: The data

import jwt
encoded = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.lBTAPFU1xxDAi2Vrusfo67ypBai0vBr6O7KOt6CJf1s'
print(jwt.decode(encoded, verify=False))


## Part 2: Justification about tampering

No its not true, because the verify signature is different for the secret of COMP1531