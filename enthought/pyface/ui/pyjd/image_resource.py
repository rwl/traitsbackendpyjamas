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

""" Enthought pyface package component
"""

# Standard library imports.
import os

# Major package imports.
from pyjamas.ui import Image

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
            icon = Image(self.absolute_path)
        else:
            image = self._get_image_not_found_image()

            icon = Image(image.absolute_path)

        return icon

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_absolute_path(self):
        # FIXME: This doesn't quite work the new notion of image size. We
        # should find out who is actually using this trait, and for what!
        # (AboutDialog uses it to include the path name in some HTML.)
        ref = self._get_ref()
        if ref is not None:
            absolute_path = os.path.abspath(self._ref.filename)

        else:
            absolute_path = self._get_image_not_found().absolute_path

        return absolute_path

#### EOF ######################################################################
