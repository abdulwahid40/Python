"""
Find differences in file contents.

"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    
    smaller_length = min(len(line1),len(line2))
    count = 0
    
    if len(line1) == 0 and len(line2) == 0:
        return IDENTICAL
      
    for idx in range(smaller_length):
        if line1[idx] != line2[idx]:
            return idx
        if len(line1) != len(line2):
            if line1[idx] == line2[idx]:
                count += 1
    
    if count == smaller_length:
        return count
    else:
        return IDENTICAL
    


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    equal_op = []
    small_len = min(len(line1),len(line2))
    if (("\n" in line1) | ("\n" in line2) | 
            ("\r" in line1) | ("\r" in line2) | (idx < 0) | (idx > small_len)):
        return ""
    else:
        if idx == 0:
            equal_op.append("^")
        for count in range(idx):
            equal_op.append("=")
            if count+1 == idx:
                equal_op.append("^")
    
    line1 = line1.strip()           
    line2 = line2.strip()
    equal_op = ''.join(equal_op)
    #formatted_string = line1 + "\n" + "=" * idx + "^" + "\n" + line2 + "\n"
    line_format = "{}{}{}".format(line1+"\n",equal_op,"\n"+line2+"\n")
    return line_format



def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    
    small_len = min(len(lines1),len(lines2))
    
    if len(lines1) == len(lines2):
        for count in range(small_len):
            idx = singleline_diff(lines1[count],lines2[count])
            if idx != -1:
                return (count,idx)
    else:
        if (len(lines1) == 0 or len(lines2) == 0):
            return(0,0)
        for count in range(small_len):
            idx = singleline_diff(lines1[count],lines2[count])
            if idx != -1:
                return (count,idx)
        return (count+1,0)
    
       
    return (IDENTICAL, IDENTICAL)



def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    cleaned_strings = []
    with open(filename) as fhand:
        lines = fhand.readlines()
    for line in lines:
        if ("\n" in line):
            line = line.strip("\n")
        if ("\r" in line):
            line = line.strip("\r")

        cleaned_strings.append(line)
    
    fhand.close()
    
    return cleaned_strings



def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    
    file1_contents = get_file_lines(filename1)
    file2_contents = get_file_lines(filename2)
    
    line_no, idx = multiline_diff(file1_contents,file2_contents)
    
    if line_no == -1:
        return "No differences\n"
    
    if (len(file2_contents) == 0):
        line_format = "Line 0:\n{}\n^\n\n".format(file1_contents[line_no])
        return line_format
    if (len(file1_contents) == 0):
        line_format = "Line 0:\n\n^\n{}\n".format(file2_contents[line_no])
        return line_format
       
    
    singleline_format = singleline_diff_format(file1_contents[line_no],
                                         file2_contents[line_no],idx)
    
    line_format = "Line {}:\n{}".format(line_no,singleline_format)
    
    return line_format 
   
  






