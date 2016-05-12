from __future__ import unicode_literals, absolute_import, print_function


class SlideShareError(Exception):
    """ SlideShare API Error Code.
    The different kind of errors thrown by the API are listed below:
        0 No API Key Provided
        1 Failed API validation
        2 Failed User authentication
        3 Missing title
        4 Missing file for upload
        5 Blank title
        6 Slideshow file is not a source object
        7 Invalid extension
        8 File size too big
        9 SlideShow Not Found
        10 User Not Found
        11 Group Not Found
        12 No Tag Provided
        13 Tag Not Found
        14 Required Parameter Missing
        15 Search query cannot be blank
        16 Insufficient permissions
        17 Incorrect parameters
        70 Account already linked
        71 No linked account found
        72 User not created
        73 Invalid Application ID
        74 Login already exists
        75 EMail already exists
        99 Account Exceeded Daily Limit
        100 Your Account has been blocked
    """
    def __init__(self, errno, errmsg):
        self.errno = errno
        self.errmsg = errmsg

    def __str__(self):
        return "SlideShareError {}: {}".format(self.errno, self.errmsg)
