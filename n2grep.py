#!/bin/python3

"""
This is a simple "egrep" variant that also ignores most comments and removes
empty lines.
"""

import sys
import re
import os

helpstr = """
n2grep [OPTION] ... PATTERN [FILE] ...
Search through files using basic regular expressions while ignoring most types
of comments.
Each option must be seperate.
Comments include both line and block based.

Options:
  -p        Print all file contents except for contents
  --help    Print help menu
  -R,-r     Recursively search through directories. Can be combined with '-p'
  
Comments ignored:
    - #
    - ;
    - //
    - \"\"\" MULTILINE TEXT \"\"\"
    - \'\'\' MULTILINE TEXT \'\'\'
    - /* MULTILINE TEXT */
"""

# Create a default state for variables
multi = False

# Regex match for single and multiline comments
# Update these variables to include other file formats
singleline_regex = r'^ *;|^ *//|^ *#|^\s*$'
multiline_regex = r' *\"\"\"| *\'\'\'| */\*| *\*/| *\<\!\-\-| *\-\-\>'


def flip():
    """
    Changes the state of multi, a True/False variable
    :return: global variable "multi"
    """
    global multi

    if multi:

        multi = False

    elif not multi:

        multi = True

    return multi


def fsearch(regex, sfile):
    """
    Primary function for regex search and stripping comments.
    :param regex: User input of the regular expression. (first user parameter)
    :param sfile: File to regex either though user input or recursion.
    :return: uncommented lines and positive regular expression results
    """
    # Print filename
    print(sfile)

    with open(sfile, 'r') as openfile:

        # Create a constant for counting line numbers
        linenumber = 0

        # Perform search function on each line
        for line in openfile:

            # Increment Line number
            linenumber += 1

            # Search for comments and blank lines
            # regex match: line starting with: ;, #, or // even if there are
            # several spaces in the beginning. Also empty lines
            if not re.search(singleline_regex, line):

                # This removes multi-line comments by searching for tags
                if re.search(multiline_regex, line) and not multi:

                    # If there is a multiline match and the value is False,
                    # flip the value of multi
                    flip()

                # Only continue with the regex if multi == False
                elif not multi:

                    if re.search(regex, line):

                        # Finally print result if matched
                        print("n{}: {}".format(linenumber, line.strip('\n')))

                # If it is the end of the multi-line, then flip multi back
                elif re.search(multiline_regex, line) and multi:

                    flip()


def recursion(regex, pdir):
    """
    Creates a recursion function that performs a search on each individual file
    as soon as it is found. Each file is added to the top of the search.
    :param pdir: Parent directory (user input)
    :param regex: Users regex
    :return: Results from fsearch and filename
    """
    all_files = []

    # Get all files and add to all_files
    for rootdir, directories, files in os.walk(pdir):

        for file in files:

            all_files.append(os.path.join(rootdir, file))

    # Perform regex on all flies
    for file in all_files:

        fsearch(regex, file)


def main(argv):
    """
    Runs the user interface portion of the program including tests
    :param argv: Passed in arguments from user (uses sys.argv())
    :return: results of all other functions and final lines
    """
    # Test the number of arguments given (filename is considered an argument)
    # If false, continue with argument parsing
    if len(sys.argv) >= 5 or len(sys.argv) == 1:

        print("WRONG NUMBER OF ARGUMENTS")
        print(helpstr)

    # option and argument parsing
    elif sys.argv[1] == "-R" or sys.argv[1] == "-r":

        if sys.argv[2] == "-p":

            recursion(r'.*', sys.argv[3])

        else:

            recursion(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "--help":

        print(helpstr)

    elif sys.argv[1] == "-p":

        # Use a "match all" regex to read file conetents without comments
        if sys.argv[2] == "-R" or sys.argv[2] == "-r":

            recursion(r'.*', sys.argv[3])

        else:

            fsearch(r'.*', sys.argv[2])

    else:

        # Perform regex
        fsearch(sys.argv[1], sys.argv[2])


main(sys.argv)
