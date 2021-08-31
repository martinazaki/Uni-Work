'''
Person Exercise
'''

class Person:
    '''
    A named person.
    '''
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = self.first_name + " " + self.last_name


    # if __name__ == "__main__":
    #     print(self.first_name)
    #     print(self.full_name)

    def __str__(self):
        result = self.full_name
        return result


# Do NOT change any code below this line

def test_simple():
    '''
    Check that Person tracks first, last and full name
    '''
    john = Person("John", "Smith")
    assert john.first_name == "John"
    assert john.last_name == "Smith"
    assert john.full_name == "John Smith"

def test_name_change():
    '''
    Check that names can be changed
    '''
    teacher = Person("Hayden", "Smith")
    teacher.first_name = "Rob"
    assert teacher.first_name == "Rob"
    assert teacher.full_name == "Rob Smith"

    teacher.last_name = "Everest"
    assert teacher.last_name == "Everest"
    assert teacher.full_name == "Rob Everest"

    teacher.full_name = "Simon Haddad"
    assert teacher.first_name == "Simon"
    assert teacher.last_name == "Haddad"

def test_single_name():
    '''
    Some people only have one name.
    '''
    madonna = Person("Madonna", None)
    assert madonna.first_name == "Madonna"
    assert madonna.last_name is None
    assert madonna.full_name == "Madonna"

def test_spaces():
    '''
    Extra spaces should be ignored.
    '''
    tutor = Person("Michelle", "Seeto")
    tutor.full_name = "Vivian  Dang" # Note one extra space

    # No spaces in name components
    assert tutor.first_name == "Vivian"
    assert tutor.last_name == "Dang"