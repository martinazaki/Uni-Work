# Lab 05

## Due: Week **5**, Sunday, 4:59 pm

## Value: 2 marks

## Setup

An individual repository for this lab has been created for you here (replace z5555555 with your own zID):

https://gitlab.cse.unsw.edu.au/z5555555/20T1-cs1531-lab05

## Project Exercises

## Exercise 1

Submit a document `team.md` where you explain how you're breaking up work between you all for this iteration, and how your separate pieces of work intersect.

You can work on this document together and all submit the same file.

## Python Exercises

## Exercise 2

This exercise should be be worked on individually. It may be in your exam, so practice it.

In `simple.py`, build a basic flask server to store a list of names using a global variable as a list. It should have routes:
 * POST /name/add
   * input { name: 'example' }
   * output { }
 * GET /names
   * input { }
   * output { names: [ 'example1', 'example2' ] }
 * DELETE /name/remove
   * input { name: 'example' }
   * output { }

For example, if the following was done:
 * POST request made to /names/add with data { name: 'Asus' }
 * POST request made to /names/add with data { name: 'Acer' }
 * POST request made to /names/add with data { name: 'Dell' }
 * GET request made to /names would return { names: [ 'Asus', 'Acer', 'Dell' ]}
 * DELETE request made to /names/remove with data { name: 'Dell' }
 * GET request made to /names would return { names: [ 'Asus', 'Acer' ]}

Ensure your code is pylint compliant.

## Exercise 3

Use urllib to write python-based tests for the flask server implemented in exercise 3 in a file `simple_test.py`.

Ensure your code is pylint compliant.

## Exercise 4

The code `drykiss.py` is unnecessarily complicated, and there is a lot of repetition. Take some time to refactor this code focusing on DRY and KISS to create a beautiful and concise piece of well understood code.

Improve the design of this code, and add a short comment or two up the top explaining what you've done and why.

Ensure your code is pylint compliant.

## Exercise 5

Write a function `factors` in `primes.py` that factorises a number into its [prime factors](https://en.wikipedia.org/wiki/Table_of_prime_factors). The program should take in a single number and the output should be the prime factors separated by a space.

```bash
16
2 2 2 2
```

```
21
3 7
```

The prime factors must be sorted in ascending order.

Write tests for your `factors` function in a file `primes_test.py`. Ensure your tests have 100% coverage. Ensure your code is pylint compliant.

## Exercise 6 (Bonus / Challenge)

This exercise should be be worked on individually. This will not be in your exam.

Observe the following jwt

*eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.lBTAPFU1xxDAi2Vrusfo67ypBai0vBr6O7KOt6CJf1s*

What data is stored in this JWT? Write it down inside `jwt.md`

This payload was originally encoded with a secret of "comp1531". Is the JWT above appropriately signed with this secret, or has it been tampered? Justify your answer in `jwt.md`

Ensure your code is pylint compliant.

## Exercise 7 (Bonus / Challenge)

Look at `encapsulate.py`. There are design imperfections with this code. relating to encapsulation (in terms of the class), and something to do with how age is calculated being rigid (in terms of it only works for 2019, and will break next year). Improve the design of this code, and add a short comment or two up the top explaining what you've done and why.

Ensure your code is pylint compliant.

## Submission

Make sure that all your work has been pushed to GitLab then submit it with:

```bash
$ 1531 submit lab05
```
