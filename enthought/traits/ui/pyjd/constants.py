#------------------------------------------------------------------------------
#  Copyright (c) 2005, Enthought, Inc.
#  Copyright (c) 2009, Richard Lincoln
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#------------------------------------------------------------------------------

""" Defines constants used by the Pyjamas implementation of the various text
    editors and text editor factories.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import sys

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Color of valid input.
OKColor = "White"

# Color to highlight input errors.
ErrorColor = "#%02x%02x%02x" % ( 255, 192, 192 )

# Color for background of windows (like dialog background color).
if (sys.platform == 'darwin'):
    WindowColor = "#%02x%02x%02x" % ( 232, 232, 232 )
else:
    WindowColor = "#%02x%02x%02x" % ( 244, 243, 238 )

# Color for background of read-only fields.
ReadonlyColor = WindowColor

# Color for background of fields where objects can be dropped.
DropColor = "#%02x%02x%02x" % ( 215, 242, 255 )

# Default dialog title.
DefaultTitle = "Edit properties"

# EOF -------------------------------------------------------------------------
