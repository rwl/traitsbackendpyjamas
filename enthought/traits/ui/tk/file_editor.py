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

""" Defines the file editors for the Tk user interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tix as tix

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.file_editor file.
from enthought.traits.ui.editors.file_editor \
    import ToolkitEditorFactory

from text_editor \
    import SimpleEditor as SimpleTextEditor

from helper \
    import TkDelegate

#------------------------------------------------------------------------------
#  'SimpleEditor' class:
#------------------------------------------------------------------------------

class SimpleEditor ( SimpleTextEditor ):
    """ Simple style of file editor.  The user can type in the filename
        manually. Alternatively, the user can press the button widget that sits
        next to the entry, which will bring up a file selection dialog.
    """

    #--------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        var           = tix.StringVar()
        control       = tix.FileEntry( parent, textvariable = var )
        factory       = self.factory
        update_object = TkDelegate( self.update_object, var = var )

        if factory.enter_set:
#            control.bind( "<Return>", update_object)
            control.config( command = update_object )

        control.bind( "<FocusOut>", update_object )

        if factory.auto_set:
           control.bind( "<Key>", self.update_object )

        self.control = control
        self.set_tooltip()

#-------------------------------------------------------------------------------
#  'CustomEditor' class:
#-------------------------------------------------------------------------------

class CustomEditor ( SimpleTextEditor ):
    """ Custom style of file editor, consisting of a file selection box.
    """

    #--------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        var           = tix.StringVar()
        control       = tix.FileSelectBox( parent, textvariable = var )
        factory       = self.factory
        update_object = TkDelegate( self.update_object, var = var )

        control.config( browsecmd = update_object )

        self.control = control
        self.set_tooltip()

# EOF -------------------------------------------------------------------------
