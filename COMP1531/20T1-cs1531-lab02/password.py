def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    '''
    
    if password == "password" or password == "iloveyou" or password == "123456":
        return "Horrible password"

    length = len(password)
    numbers = 0
    uppercase = 0
    lowercase = 0

    for m in password:
        if (m.isuppercase()) == True:
            uppercase += 1
        if (m.islowercase()) == True:
            lowercase += 1
        if (m.isdigit()) == True:
            numbers += 1

    if length >= 12 and uppercase >= 1 and lowercase >= 1 and numbers >= 1:
        return "Strong password"
    
    elif length >= 8 and numbers >= 1:
        return "Moderate password"

    else:
        return "Poor password"
    
    pass

if __name__ == '__main__':
    print(check_password("ihearttrimesters"))
    # What does this do?

def password_tests():
    assert(check_password("Thisisawesome123") == "Strong password")   
    assert(check_password("Bullwinkle2468") == "Strong password") 
    assert(check_password("isthisgood123") == "Moderate password")
    assert(check_password("ILOVEUNI1") == "Moderate password")
    assert(check_password("123456") == "Horrible password")
    assert(check_password("password") == "Horrible password")