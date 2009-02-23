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

""" Defines the base class for Pyjamas editors.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import sys

from pyjamas import Window
from pyjamas.ui import RootPanel
from Tooltip import TooltipListener

from enthought.traits.api \
    import HasTraits, Int, Instance, Str, Callable

from enthought.traits.ui.editor \
    import Editor as UIEditor

from constants \
    import WindowColor, OKColor, ErrorColor

#------------------------------------------------------------------------------
#  'Editor' class:
#------------------------------------------------------------------------------

class Editor ( UIEditor ):
    """ Base class for Pyjamas editors for Traits-based UIs.
    """

    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Style for embedding control in a sizer:
    layout_style = Str( 'both' )

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
        new_value = self.str_value
        if self.control.getText() != new_value:
            self.control.setText( new_value )

    #--------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #--------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
        Window.alert( self.description + ' value error' + str( excp ) )

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

        listener = TooltipListener( desc )
        control.addMouseListener( listener )

        return True

    #--------------------------------------------------------------------------
    #  Handles the 'enabled' state of the editor being changed:
    #--------------------------------------------------------------------------

    def _enabled_changed ( self, enabled ):
        """ Handles the **enabled** state of the editor being changed.
        """
        control = self.control
        if control is not None:
            control.setEnabled( enabled )


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
                    item._ok_color = item.getStyleName( "color" )
            else:
                color = getattr( item, '_ok_color', None )
                if color is None:
                    color = OKColor
                    if isinstance( item, RootPanel ):
                        color = WindowColor

            item.setStyleName( element = "color", style = color )

    #--------------------------------------------------------------------------
    #  Handles the editor's invalid state changing:
    #--------------------------------------------------------------------------

    def _invalid_changed ( self, state ):
        """ Handles the editor's invalid state changing.
        """
        self.set_error_state()

# EOF -------------------------------------------------------------------------
