#------------------------------------------------------------------------------
#
#  Copyright (c) 2009, Richard W. Lincoln
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Author: Richard W. Lincoln
#  Date:   29/01/2009
#
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

OKColor = "White"

ErrorColor = "#%02x%02x%02x" % ( 255, 192, 192 )

if (sys.platform == 'darwin'):
    WindowColor = "#%02x%02x%02x" % ( 232, 232, 232 )
else:
    WindowColor = "#%02x%02x%02x" % ( 244, 243, 238 )

ReadonlyColor = WindowColor

# EOF -------------------------------------------------------------------------
