#------------------------------------------------------------------------------
#
#  Copyright (c) 2008, Richard W. Lincoln
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Author: Richard W. Lincoln
#  Date:   29/01/2008
#
#------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Standard library imports.
import os

# Major package imports.
import Tkinter

# Enthought library imports.
from enthought.resource.api import ResourceFactory


class PyfaceResourceFactory(ResourceFactory):
    """ The implementation of a shared resource manager. """

    ###########################################################################
    # 'ResourceFactory' toolkit interface.
    ###########################################################################

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        return Tkinter.PhotoImage(filename)


    def image_from_data(self, data, filename=None):
        """ Creates an image from the specified data. """

        return Tkinter.PhotoImage(data)

#### EOF ######################################################################
