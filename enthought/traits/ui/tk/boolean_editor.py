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

""" Defines the various Boolean editors for the wxPython user interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tkinter

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

#------------------------------------------------------------------------------
#  'SimpleEditor' class:
#------------------------------------------------------------------------------

class SimpleEditor ( Editor ):
    """ Simple style of editor for Boolean values, which displays a check box.
    """
    #--------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
#        self.control = wx.CheckBox( parent, -1, '' )
#        wx.EVT_CHECKBOX( parent, self.control.GetId(), self.update_object )
        self.var = var = Tkinter.IntVar()
        self.control = Tkinter.Checkbutton( parent, variable = var )
        self.set_tooltip()

    #--------------------------------------------------------------------------
    #  Handles the user clicking on the checkbox:
    #--------------------------------------------------------------------------

    def update_object ( self, event ):
        """ Handles the user clicking the checkbox.
        """
        self.value = (self.var.get() != 0)

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        self.var.set( self.value )

#------------------------------------------------------------------------------
#  'ReadonlyEditor' class:
#------------------------------------------------------------------------------

#class ReadonlyEditor ( Editor ):
#    """ Read-only style of editor for Boolean values, which displays static text
#    of either "True" or "False".
#    """
#    #--------------------------------------------------------------------------
#    #  Finishes initializing the editor by creating the underlying toolkit
#    #  widget:
#    #--------------------------------------------------------------------------
#
#    def init ( self, parent ):
#        """ Finishes initializing the editor by creating the underlying toolkit
#            widget.
#        """
#        self.control = wx.TextCtrl( parent, -1, '', style = wx.TE_READONLY )
#        self.control.SetBackgroundColour( ReadonlyColor )
#
#    #--------------------------------------------------------------------------
#    #  Updates the editor when the object trait changes external to the editor:
#    #
#    #  (Should normally be overridden in a subclass)
#    #--------------------------------------------------------------------------
#
#    def update_editor ( self ):
#        """ Updates the editor when the object trait changes externally to the
#            editor.
#        """
#        if self.value:
#            self.control.SetLabel( 'True' )
#        else:
#            self.control.SetLabel( 'False' )

