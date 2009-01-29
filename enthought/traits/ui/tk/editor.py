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

""" Defines the base class for Tkinter editors.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import sys

import Tkinter
import tkMessageBox

from enthought.traits.api \
    import HasTraits, Int, Instance, Str, Callable

# CIRCULAR IMPORT FIXME:
# We are importing from the source instead of from the api in order to
# avoid circular imports. The 'toolkit.py' file imports from 'helper' which in
# turns imports from this file. Therefore, trying to import
# 'enthought.traits.ui.wx' (which imports the toolkit) will lead to importing
# all of the editor factories declared in enthought.traits.ui.api. In addition,
# some of the editor factories have a Color trait defined, and this will lead
# to an import of the wx 'toolkit' causing a circular import problem.
# Another solution could be to move the GroupEditor object from helper to this
# file.
from enthought.traits.ui.editor \
    import Editor as UIEditor

#from constants \
#    import WindowColor, OKColor, ErrorColor

OKColor = "White"

ErrorColor = "#%02x%02x%02x" % ( 255, 192, 192 )

if (sys.platform == 'darwin'):
    WindowColor = "#%02x%02x%02x" % ( 232, 232, 232 )
else:
    WindowColor = "#%02x%02x%02x" % ( 244, 243, 238 )

#------------------------------------------------------------------------------
#  'Editor' class:
#------------------------------------------------------------------------------

class Editor ( UIEditor ):
    """ Base class for wxPython editors for Traits-based UIs.
    """

    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Style for embedding control in a sizer:
    layout_style = Str( Tkinter.BOTH )

    # The maximum extra padding that should be allowed around the editor:
    border_size = Int( 4 )

    #--------------------------------------------------------------------------
    #  Handles the 'control' trait being set:
    #--------------------------------------------------------------------------

    def _control_changed ( self, control ):
        """ Handles the **control** trait being set.
        """
        if control is not None:
            control._editor = self

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        control = self.control
        new_value = self.str_value
        if control.get() != new_value:
            control.delete( 0, len(control,get()) )
            control.insert( 0, new_value )

    #--------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #--------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
#        top = Tkinter.Toplevel(self.control)
#        top.title = (self.description + ' value error')
#
#        Tkinter.Label( top, text = str( excp ) ).pack()
#        Tkinter.Button( top, text="OK", command=lambda e: e.widget.destroy())
#
#        top.grab_set()
#        top.focus_set()
#        self.control.wait_window(top)
#
#        top.mainloop()
        tkMessageBox.showinfo( self.description + ' value error', str( excp ) )

    #--------------------------------------------------------------------------
    #  Sets the tooltip for a specified control:
    #--------------------------------------------------------------------------

    def set_tooltip ( self, control = None ):
        """ Sets the tooltip for a specified control.
        """
        desc = self.description
        if desc == '':
            desc = self.object.base_trait( self.name ).desc
            if desc is None:
                return False

            desc = 'Specifies ' + desc

        if control is None:
            control = self.control

        ToolTip( control, text=desc )

        return True

    #--------------------------------------------------------------------------
    #  Handles the 'enabled' state of the editor being changed:
    #--------------------------------------------------------------------------

    def _enabled_changed ( self, enabled ):
        """ Handles the **enabled** state of the editor being changed.
        """
        control = self.control
        if control is not None:
            if enabled:
                control.config( state=Tkinter.NORMAL )
            else:
                control.config( state=Tkinter.DISABLED )

#            control.Refresh()

    #--------------------------------------------------------------------------
    #  Handles the 'visible' state of the editor being changed:
    #--------------------------------------------------------------------------

    def _visible_changed ( self, visible ):
        """ Handles the **visible** state of the editor being changed.
        """
        raise NotImplementedError

    #--------------------------------------------------------------------------
    #  Returns the editor's control for indicating error status:
    #--------------------------------------------------------------------------

    def get_error_control ( self ):
        """ Returns the editor's control for indicating error status.
        """
        return self.control

    #--------------------------------------------------------------------------
    #  Returns whether or not the editor is in an error state:
    #--------------------------------------------------------------------------

    def in_error_state ( self ):
        """ Returns whether or not the editor is in an error state.
        """
        return False

    #--------------------------------------------------------------------------
    #  Sets the editor's current error state:
    #--------------------------------------------------------------------------

    def set_error_state ( self, state = None, control = None ):
        """ Sets the editor's current error state.
        """
        if state is None:
            state = self.invalid
        state = state or self.in_error_state()

        if control is None:
            control = self.get_error_control() or []

        if not isinstance( control, list ):
            control = [ control ]

        for item in control:
            if state:
                color = ErrorColor
                if getattr( item, '_ok_color', None ) is None:
                    item._ok_color = item.cget("bg")
            else:
                color = getattr( item, '_ok_color', None )
                if color is None:
                    color = OKColor
                    if isinstance( item, Tkinter.Frame ):
                        color = WindowColor

            item.config( bg=color )

    #--------------------------------------------------------------------------
    #  Handles the editor's invalid state changing:
    #--------------------------------------------------------------------------

    def _invalid_changed ( self, state ):
        """ Handles the editor's invalid state changing.
        """
        self.set_error_state()

# EOF -------------------------------------------------------------------------
