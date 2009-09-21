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
#  Date:   22/02/2009
#
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
