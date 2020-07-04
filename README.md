# n2grep
This is a simple "egrep" variant that also ignores most comments and removes
empty lines.


## Usage

n2grep [OPTION] ... PATTERN [FILE] ...
Search through files using basic regular expressions while ignoring most types
of comments.
Each option must be seperate.
Comments include both line and block based.

* Options:
  * -p        Print all file contents except for contents
  * --help    Print help menu
  * -R,-r     Recursively search through directories. Can be combined with '-p'
  
* Comments ignored:
  * \#
  * \;
  * \/\/
  * \"\"\" MULTILINE TEXT \"\"\"
  * \'\'\' MULTILINE TEXT \'\'\'
  * \/\* MULTILINE TEXT \*\/
