#------------------------------------------------------------------------------
#  Copyright (c) 2005, Enthought, Inc.
#  Copyright (c) 2009, Richard W. Lincoln
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

""" Defines the various styles of editors used in a Traits-based user
    interface.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from pyjamas.ui import \
    TextArea, TextBox

from editor \
    import Editor

from constants \
    import WindowColor

#------------------------------------------------------------------------------
#  'ReadonlyEditor' class:
#------------------------------------------------------------------------------

class ReadonlyEditor ( Editor ):
    """ Base class for read-only style editors, which displays a read-only text
        field, containing a text representation of the object trait value.
    """

    #--------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        if (self.item.resizable is True) or (self.item.height != -1.0):
            control = TextArea()
        else:
            control = TextBox()

        control.setEnabled( False )
        control.setStyleName( element = "color", style = WindowColor )

        self.control = control
        self.set_tooltip()

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        new_value = self.str_value

        if self.control.getText() != new_value:
            self.control.setText( new_value )

# EOF -------------------------------------------------------------------------
