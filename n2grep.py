#!/home/phate/anaconda3/bin/python3

"""
This is a simple "egrep" variant that also ignores most comments and removes
empty lines.
"""

import sys
import re

helpstr = """
n2grep [OPTION] ... PATTERN [FILE] ...
Search through files using basic regular expressions while ignoring most types
of comments.
Comments include both line and block based.

Options:
  -p        Print all file contents except for contents
  --help    Print help menu
  -R,-r     Recursively search through directories. Cannot be combined with '-p'
  
Comments ignored:
    - #
    - ;
    - //
    - \"\"\" MULTILINE TEXT \"\"\"
    - \'\'\' MULTILINE TEXT \'\'\'
    - /* MULTILINE TEXT */
"""

# Create a default state for variable
multi = False


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
            if not re.search(r'^ *;|^ *//|^ *#|^\s*$', line):

                # This removes multi-line comments by searching for tags
                if re.search(r' *\"\"\"| *\'\'\'| */\*| *\*/', line) and not multi:

                    # If there is a multiline match and the value is False,
                    # flip the value of multi
                    flip()

                # Only continue with the regex if multi == False
                elif not multi:

                    if re.search(regex, line):

                        # Finally print result if matched
                        print("n{}: {}".format(linenumber, line.strip('\n')))

                # If it is the end of the multi-line, then flip multi back
                elif re.search(r' *\"\"\"| *\'\'\'| */\*| *\*/', line) and multi:

                    flip()


def main(argv):
    """
    Runs the user interface portion of the program including tests
    :param argv: Passed in arguments from user (uses sys.argv())
    :return: results of all other functions and final lines
    """
    # Test the number of arguments given (filename is considered an argument)
    if len(sys.argv) >= 5 or len(sys.argv) == 1:

        print("WRONG NUMBER OF ARGUMENTS")
        print(helpstr)

    # option and argument parsing
    if sys.argv[1] == "-R" or sys.argv[1] == "-r":

        patern = sys.argv[2]
        directory = sys.argv[3]

        print("RECURSIVE AINT DONE")

    elif sys.argv[1] == "--help":

        print(helpstr)

    elif sys.argv[1] == "-p":

        # Use a "match all" regex to read file conetents without comments
        fsearch(r'.*', sys.argv[2])

    else:

        # Perform regex
        fsearch(sys.argv[1], sys.argv[2])


main(sys.argv)
