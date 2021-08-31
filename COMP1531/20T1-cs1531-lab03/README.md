# Lab 03

## Due: Week **4**, Sunday, 5:00 pm

**NOTE: You have two weeks to do this lab**

## Value: 2 marks

## Aim

* Further practice programming in python
* Further practise using pytest
* Working with objects in python

## Setup

An individual repository for this lab has been created for you here (replace z5555555 with your own zID):

https://gitlab.cse.unsw.edu.au/z5555555/20T1-cs1531-lab03

## Python Exercises

## Exercise 1

Open `president.py` and write some python code to make the following changes to the dictionary:
 * Remove "Hayden" from the list of "staff" in the `president` structure (we don't like him)
 * Sort the list of "staff" in the president structure in alphabetical order
 * Add a new key to the president structure called "marks", which itself consists of a dictionary that contains a key => value mapping of 'term' => mark. E.G. { "20T1" : 78 }. Add the following marks:
   * 20T1: 77
   * 20T2: 88
   * 20T3: 99

Note: You are not allowed to edit the structure directly. You must write your code between the two comments specified in `president.py`

## Exercise 2

Open `marks.py`. Currently, the program outputs the average homework, quiz, and test marks across all of the students as 0. Modify the main component of the code (underneath line 22) to accurately computer the averages from the dictionary at the top of the file. The averages are for the average of homework, quizzes, and tests, across ALL students.

## Exercise 3

Open `prefix.py` and complete the function `prefix_search()` according to its documentation.

Some tests have been added in `prefix_test.py`. Ensure your solution passes those tests then write some of your own such that you have complete test coverage.

## Exercise 4

In the lecture you were introduced to the `date` class and objects constructed from it. Python also comes with classes for `time`, a time independent of a particular day, and `datetime`, a combination of a date and a time.

Open `timetable.py` and complete the function `timetable()` according to its documentation.

Write some tests in a new file you create called `timetable_test.py`.

*To receive full marks for this question you must achieve 100% coverage using python3-coverage, as described in lectures.*

## Exercise 5

Complete a function in `roman.py` that prints out the decimal value of a Roman numeral. You may assume the Roman numeral is in the "standard" form, i.e. any digits involving 4 and 9 will always appear in the subtractive form.

The file `roman_main.py` has been given with the expected outputs of use function use in the comments beside. 

Hints:
 * Use a loop to iterate through the Roman numeral to figure out their value.
 * Use a list of tuples to store the string characters and their respective values, compare the characters from the input to this list.
 * Use a while loop so you can manually control the indices.

You are expected to write tests for `roman.py` inside that file using pytest-3.

*To receive full marks for this question you must achieve 100% coverage in roman.py using python3-coverage, as described in lectures.*

## Exercise 6 (Challenge)

Write a program `magic.py` that determines whether an array of n by n integers is a magic square.

Example input

```bash
$ python3 magicsquare.py
3
8 1 6
3 5 7
4 9 2
Magic square
```

The program's output is one of the following statements:
 * "Magic square" (if the input is a magic square)
 * "Invalid data: missing or repeated number" (if there is a missing or repeated number)
 * "Invalid data: inconsistent sums" (if no numbers are missing or incorrect, but their sums are not all the same)

## Submission

Make sure that all your work has been pushed to GitLab then submit it with:

```bash
$ 1531 submit lab03
```