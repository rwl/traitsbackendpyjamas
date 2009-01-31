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
#  Date:   30/01/2009
#
#------------------------------------------------------------------------------

""" Defines the various text editors for the Tk user interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import logging

import Tkinter as tk

from enthought.traits.api \
    import TraitError

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.text_editor file.
from enthought.traits.ui.editors.text_editor \
    import ToolkitEditorFactory, evaluate_trait

from editor \
    import Editor

from editor_factory \
    import ReadonlyEditor as BaseReadonlyEditor

from constants \
    import OKColor

from helper \
    import TkDelegate

#------------------------------------------------------------------------------
#  Start logging:
#------------------------------------------------------------------------------

logger = logging.getLogger( __name__ )

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Readonly text editor with view state colors:
HoverColor = "Grey"
DownColor  = "White"

#-------------------------------------------------------------------------------
#  'SimpleEditor' class:
#-------------------------------------------------------------------------------

class SimpleEditor ( Editor ):
    """ Simple style text editor, which displays a text field.
    """

    # Flag for window styles:
    base_style = 0

    # Background color when input is OK:
    ok_color = OKColor

    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Function used to evaluate textual user input:
    evaluate = evaluate_trait

    #--------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        factory       = self.factory
        var           = tk.StringVar()
        update_object = TkDelegate( self.update_object, var = var )

        multi_line = factory.multi_line and (not factory.password)

        if multi_line:
            control = tk.Text( parent, textvariable = var )
        else:
            control = tk.Entry( parent, textvariable = var )

        # Controls how to display the contents of the widget.
        if factory.password:
            control.config( show = "*" )

        if multi_line:
            self.scrollable = True

        if factory.enter_set and (not multi_line):
            control.bind( "<Return>", update_object )

        control.bind( "<FocusOut>", update_object )

        if factory.auto_set:
           control.bind( "<Key>", self.update_object )

        self.control = control
        self.set_tooltip()

    #--------------------------------------------------------------------------
    #  Handles the user entering input data in the edit control:
    #--------------------------------------------------------------------------

    def update_object ( self, event ):
        """ Handles the user entering input data in the edit control.
        """
        if (not self._no_update) and (self.control is not None):
            try:
                self.value = self._get_user_value()
                self.control.configure( bg = OKColor )

                if self._error is not None:
                    self._error     = None
                    self.ui.errors -= 1

                self.set_error_state( False )

            except TraitError, excp:
                pass

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        user_value = self._get_user_value()
        try:
            unequal = bool( user_value != self.value )
        except ValueError:
            # This might be a numpy array.
            unequal = True

        if unequal:
            self._no_update = True
            var.set ( self.str_value )
            self._no_update = False

        if self._error is not None:
            self._error     = None
            self.ui.errors -= 1
            self.set_error_state( False )

    #--------------------------------------------------------------------------
    #  Gets the actual value corresponding to what the user typed:
    #--------------------------------------------------------------------------

    def _get_user_value ( self ):
        """ Gets the actual value corresponding to what the user typed.
        """
        var = self.control.cget('textvariable' )
        value = var.get()
        try:
            value = self.evaluate( value )
        except:
            logger.exception( 'Could not evaluate %r in TextEditor' %
                              ( value, ) )

        try:
            ret = self.factory.mapping.get( value, value )
        except TypeError:
            # The value is probably not hashable:
            ret = value

        return ret

    #--------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #--------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
        if self._error is None:
            self.control.config( bg = ErrorColor )
            self._error     = True
            self.ui.errors += 1

        self.set_error_state( True )

    #--------------------------------------------------------------------------
    #  Returns whether or not the editor is in an error state:
    #--------------------------------------------------------------------------

    def in_error_state ( self ):
        """ Returns whether or not the editor is in an error state.
        """
        return (self.invalid or self._error)

#-------------------------------------------------------------------------------
#  'CustomEditor' class:
#-------------------------------------------------------------------------------

class CustomEditor ( SimpleEditor ):
    """ Custom style of text editor, which displays a multi-line text field.
    """

    pass

#-------------------------------------------------------------------------------
#  'ReadonlyEditor' class:
#-------------------------------------------------------------------------------

class ReadonlyEditor ( BaseReadonlyEditor ):
    """ Read-only style of text editor, which displays a read-only text field.
    """

    pass


TextEditor = SimpleEditor

# EOF -------------------------------------------------------------------------
