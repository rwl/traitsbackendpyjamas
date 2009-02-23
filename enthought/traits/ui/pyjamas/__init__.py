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
#  Date:   23/02/2009
#
#------------------------------------------------------------------------------

""" Defines the concrete implementations of the traits Toolkit interface for
    the Pyjamas web application user interface.
"""

__import__('pkg_resources').declare_namespace(__name__)

#------------------------------------------------------------------------------
#  Define the reference to the exported GUIToolkit object:
#------------------------------------------------------------------------------

import toolkit

# Reference to the GUIToolkit object for Pyjamas.
toolkit = toolkit.GUIToolkit()

# EOF -------------------------------------------------------------------------