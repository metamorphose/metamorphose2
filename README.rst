**************
Métamorphose 2
**************

Métamorphose is a graphical mass renaming program for files and folders.

These are the command line options::

  -h,  --help       Show the help screen and exit
  -t,  --timer      Show time taken to complete operations
  -d,  --debug      Show debugging information
  -p=, --path=      Specify a directory to load
  -c=, --config=    Specify a Metamorphose2 config file to load
  -a=, --auto=      Specify automatic mode level (when also using -c option):
                      0 = do not preview items (will overide preferences)
                      1 = auto preview items (will overide preferences)
                      2 = auto rename items
                      3 = auto rename items and exit on success
  -l=, --language=  Overide prefered interface language:
                      en_US
                      fr

If no other options are given, you may specify a path to open::

  $ metamorphose2 /srv/samba/Windows Likes Spaces

