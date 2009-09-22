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

""" Defines the various Boolean editors for the Pyjamas user interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from pyjamas.ui.Checkbox import CheckBox
from pyjamas.ui.Label import Label

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.boolean_editor file.
from enthought.traits.ui.editors.boolean_editor \
    import ToolkitEditorFactory

from editor \
    import Editor

# This needs to be imported in here for use by the editor factory for boolean
# editors (declared in enthought.traits.ui). The editor factory's text_editor
# method will use the TextEditor in the ui.
from text_editor \
    import SimpleEditor as TextEditor

from constants \
    import ReadonlyColor

from helper \
    import PyjsDelegate

#------------------------------------------------------------------------------
#  'SimpleEditor' class:
#------------------------------------------------------------------------------

class SimpleEditor ( Editor ):
    """ Simple style of editor for Boolean values, which displays a check box.
    """
    #--------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        self.control = control = CheckBox()
        parent.add( control )
#        control.addClickListener( self.update_object )
        self.set_tooltip()

    #--------------------------------------------------------------------------
    #  Handles the user clicking on the checkbox:
    #--------------------------------------------------------------------------

    def update_object ( self, delegate ):
        """ Handles the user clicking the checkbox.
        """
        self.value = (delegate.isChecked() != 0)

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        self.control.setChecked( self.value )

#-------------------------------------------------------------------------------
#  'ReadonlyEditor' class:
#-------------------------------------------------------------------------------

class ReadonlyEditor ( Editor ):

    #---------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        control = Label( text = '' )
        parent.add( control )
        self.control = control

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        self.control.setText( text = [ 'False', 'True' ][ self.value ] )

# EOF -------------------------------------------------------------------------
