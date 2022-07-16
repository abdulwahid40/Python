# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 08:45:41 2022

@author: AbdulWahid
"""

"""

Coderbyte progamming challenge

Prime Checker
Have the function PrimeChecker(num) take num and return 1 if any arrangement of
num comes out to be a prime number, otherwise return 0. For example: if num is 910,
the output should be 1 because 910 can be arranged into 109 or 019, both of which are primes.
Examples
Input: 98
Output: 1
Input: 598
Output: 1
Browse Resources
Search for any help or documentation you might need for this problem. 
For example: array indexing, Ruby hash tables, etc.

"""

print("Hello World!")

def is_prime(num):
  flag = True
  if num > 1:
    for i in range(2,num):
      if (num % i) == 0:
        flag = False
        return flag
    return flag




def PrimeChecker(num):

  import itertools
  temp = str(num)
  for num in itertools.permutations(temp, len(temp)):
    join_num = int("".join(num))
    if (is_prime(join_num)):
      return 1
  return 0


# keep this function call here 
print(PrimeChecker(input()))