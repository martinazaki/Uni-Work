

def reverse_words(string_list):

    wordsInput = string_list.split(" ")
    wordsInput = wordsInput[-1::-1]
    output = ' '.join(wordsInput)
    return output

def reverse_tests()
    assert(check_reverse("Hello how are you") == "you are how Hello")
    assert(check_reverse("I am very excited") == "excted very am I")
    assert(check_reverse("I am tired") == "tired am I")
    assert(check_reverse("I am quite hungry") == "hungry quie am I")
    assert(check_reverse("Keen to graduate soon") == "soon graduate to Keen")