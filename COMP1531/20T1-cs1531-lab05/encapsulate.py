
import datetime

class Student:
    def __init__(self, firstName, lastName, birthYear):
        self.name = firstName + " " + lastName
        self.birthYear = birthYear

    def name(self):
    	return self.name

    def age(self):
    	return datetime.datetime.now().year - self.birthYear

if __name__ == '__main__':
    s = Student("Rob", "Everest", 1961)
    print(f"{s.name()} is {s.age()} old")
