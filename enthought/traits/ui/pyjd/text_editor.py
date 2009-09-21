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

""" Defines the various text editors for the Pyjamas web toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import logging

from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.PasswordTextBox import PasswordTextBox

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
    import PyjsDelegate

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

    # Flag for window style:
    multi_line = False

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
#        update_object = PyjsDelegate( self.update_object, var = var )

        multi_line = (factory.multi_line and (not factory.password)) \
                                         or self.multi_line

        if factory.password:
            control = PasswordTextBox()
        elif multi_line:
            control = TextArea()
        else:
            control = TextBox()

        if multi_line:
            self.scrollable = True

        if factory.enter_set and (not multi_line):
            control.addKeyboadListener(self.update_object, "<Return>")

        control.addFocusListener( self.update_object )

#        if factory.auto_set:
#           control.addKeyboadListener( self.update_object )

        parent.add(control)
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
                self.control.setStyleName( "color", OKColor )

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
            self.control.setText( self.str_value )
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
        value = self.control.getText()
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
            self.control.setStyleName( "color", ErrorColor )
            self._error = True
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

    # Flag for window style:
    multi_line = True

#-------------------------------------------------------------------------------
#  'ReadonlyEditor' class:
#-------------------------------------------------------------------------------

class ReadonlyEditor ( BaseReadonlyEditor ):
    """ Read-only style of text editor, which displays a read-only text field.
    """

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        new_value = self.str_value

        if self.factory.password:
            new_value = '*' * len( new_value )

        if self.control.getText() != new_value:
            self.control.setText( new_value )


TextEditor = SimpleEditor

# EOF -------------------------------------------------------------------------
