"""
Coderbyte Challenge of Palindrome Creator

Palindrome Creator
Have the function PalindromeCreator(str) take the str parameter being passed and determine if it is possible to create a 
palindromic string of minimum length 3 characters by removing 1 or 2 characters. 
For example: if str is "abjchba" then you can remove the characters jc to produce "abhba" which is a palindrome.
For this example your program should return the two characters that were removed with no delimiter a
nd in the order they appear in the string, so jc. If 1 or 2 characters cannot be removed to produce a palindrome, 
then return the string not possible.

If the input string is already a palindrome, your program should return the string palindrome. 
Your program should always remove the characters that appear earlier in the string. 
In the example above, you can also remove ch to form a palindrome but jc appears first, so the correct answer is jc.

The input will only contain lowercase alphabetic characters. Your program should always attempt to create the 
longest palindromic substring by removing 1 or 2 characters (see second sample test case as an example). 
The 2 characters you remove do not have to be adjacent in the string.
Examples
Input: "mmop"
Output: not possible
Input: "kjjjhjjj"
Output: k
Browse Resources
Search for any help or documentation you might need for this problem. For example: array indexing, Ruby hash tables, etc.

"""




def is_palindrome(string):
  if (string==string[::-1]):
    return True
  else:
    return False
  

def single_char_remove(string):
  for i in range(len(string)):
    ch = string[i]
    new_string = string[:i] + string[i+1:]
    if (len(new_string)) > 2:
      if (is_palindrome(new_string)):
        return ch
  else:
    return False


def double_char_remove(string):
  for i in range(len(string)):
    for j in range(i+1, len(string)):
      string_list = list(string)
      string_list[i] = ''
      string_list[j] = ''
      result = "".join(string_list)
      if (len(result)) > 2:
        if (is_palindrome(result)):
          ch_tuple = (string[i], string[j])
          res_string = "".join(ch_tuple)
          return res_string

  return False


def PalindromeCreator(strParam):

  if len(strParam) > 2:
    if (is_palindrome(strParam)):
      print("palindrome")
    else:
      result = single_char_remove(strParam)
      if (result):
        return result
      else:
        result_double = double_char_remove(strParam)
        if (type(result_double) == type(True)):
          return "not possible"
        else:
          return result_double
  else:
    print("String is less than 3 characters")
  


  # code goes here
  

# keep this function call here 
print(PalindromeCreator(input()))