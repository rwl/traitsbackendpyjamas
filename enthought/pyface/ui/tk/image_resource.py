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
from enthought.traits.api import Any, HasTraits, implements, List, Property
from enthought.traits.api import Unicode

# Local imports.
from enthought.pyface.i_image_resource import IImageResource, MImageResource


class ImageResource(MImageResource, HasTraits):
    """ The toolkit specific implementation of an ImageResource.  See the
    IImageResource interface for the API documentation.
    """

    implements(IImageResource)

    #### Private interface ####################################################

    # The resource manager reference for the image.
    _ref = Any

    #### 'ImageResource' interface ############################################

    absolute_path = Property(Unicode)

    name = Unicode

    search_path = List

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    def create_bitmap(self, size=None):
        return self.create_image(size)#.ConvertToBitmap()


    def create_icon(self, size=None):
        ref = self._get_ref(size)

        if ref is not None:
            icon = Tkinter.PhotoImage(self.absolute_path)
        else:
            image = self._get_image_not_found_image()

            # You can use a PhotoImage instance everywhere Tkinter accepts an
            # image object.
            icon = Tkinter.PhotoImage(image.absolute_path)

        return icon

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_absolute_path(self):
        # FIXME: This doesn't quite wotk the new notion of image size. We
        # should find out who is actually using this trait, and for what!
        # (AboutDialog uses it to include the path name in some HTML.)
        ref = self._get_ref()
        if ref is not None:
            absolute_path = os.path.abspath(self._ref.filename)

        else:
            absolute_path = self._get_image_not_found().absolute_path

        return absolute_path

#### EOF ######################################################################
