'''
Tests for the core functionality of the helpr application
'''
import pytest
# Don't change this import line below. If your tests are black-box tests then
# you don't require any more functions from the module than these
from helpr import make_request, queue, remaining, help, resolve, cancel, revert, reprioritise, end

def test_sanity():
    '''
    A simple sanity test of the system.
    '''
    # DO NOT CHANGE THIS TEST! If you feel you have to change this test then
    # your functions have not been implemented correctly.
    student1 = "z1234567"
    description1 = "I don't understand how 'global' works in python"
    student2 = "z7654321"
    description2 = "What's the difference between iterator and iterable?"

    # Queue is initially empty
    assert queue() == []

    # Student 1 makes a request
    make_request(student1, description1)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"}]
    assert remaining(student1) == 0

    # Student 2 makes a request
    make_request(student2, description2)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    assert remaining(student1) == 0
    assert remaining(student2) == 1

    # Student 1 gets help
    help(student1)
    assert queue() == [{"zid": student1, "description": description1, "status": "receiving"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    # Student 2 is now the only student "waiting" in the queue, so they have no
    # one remaining in front of them
    assert remaining(student2) == 0

    # Student 1 has their problem resolved
    resolve(student1)
    # Only student 2 is left in the queue
    assert queue() == [{"zid": student2, "description": description2, "status": "waiting"}]

    # Student is helped and their problem is resolved
    help(student2)
    resolve(student2)
    assert queue() ==[]

    # End the session
    end()

def test_make_request():
    ''' Test for make request function'''
    student1 = "z1234567"
    description1 = " "
    description2 = "I don't understand some stuff in python"

    with pytest.raises (ValueError):
        make_request(student1, description1)

    with pytest.raises (KeyError):
        make_request(student1, description2)

def test_queue():
    ''' Test for queue function'''
    pass

def test_remaining():
    ''' Test for remaining function'''
    student1 = "z1234567"
    description1 = "What is python"

    with pytest.raises (KeyError):
        make_request(student1, description1)
        assert queue() == [{"zid": student1, "description": description1, "status": "receiving"}]

def test_help():
    ''' Test for help function'''
    student1 = "z1234567"
    description1 = "What is http?"

    with pytest.raises (KeyError):
        make_request(student1, description1)
        assert queue() == [{"zid": student1, "description": description1, "status": "receiving"}]

def test_resolve():
    ''' Test for resolve function'''
    student1 = "z1234567"
    description1 = "What is flask?"

    with pytest.raises (KeyError):
        make_request(student1, description1)
        assert queue() == [{"zid": student1, "description": description1, "status": "waiting"}]

def test_cancel():
    ''' Test for cancel function'''
    student1 = "z1234567"
    description1 = "I don't understand dict"

    with pytest.raises (KeyError):
        make_request(student1, description1)
        assert queue() == [{"zid": student1, "description": description1, "status": "receiving"}]  

def test_revert():
    ''' Test for queue function'''
    student1 = "z1234567"
    description1 = "Is python different to python3"

    with pytest.raises (KeyError):
        make_request(student1, description1)
        assert queue() == [{"zid": student1, "description": description1, "status": "waiting"}]  

def test_reprioritise():
    ''' Test for reprioritise function'''
    pass

def test_end():
    ''' Test for end function'''
    pass          