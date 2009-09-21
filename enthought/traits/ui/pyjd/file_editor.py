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

""" Defines the file editors for the Pyjamas web interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from pyjamas.ui \
    import FileUpload, FormPanel, Button

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.file_editor file.
from enthought.traits.ui.editors.file_editor \
    import ToolkitEditorFactory

from text_editor \
    import SimpleEditor as SimpleTextEditor

from helper \
    import PyjsDelegate

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
        # Create a FormPanel and point it at a service.
        control = FormPanel()
        control.setAction( self.update_object )

        # Because we're going to add a FileUpload widget, we'll need to set the
        # form to use the POST method, and multipart MIME encoding.
        control.setEncoding(FormPanel.ENCODING_MULTIPART)
        control.setMethod(FormPanel.METHOD_POST)

        upload = FileUpload()
        upload.setName("File...")
        factory = self.factory
        control.add(upload)

        # Add a 'submit' button.
        control.add(Button("Submit", self))

#        if factory.enter_set:
#            control.addFormHandler( self.update_object, "<Return>" )

#        control.addFocusListener( self.update_object )

#        if factory.auto_set:
#           control.addKeyboadListener( self.update_object )

        parent.add( control )
        self.control = control
        self.set_tooltip()


    def onClick(self, sender):
        self.control.submit()

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
        control = FileUpload()
        factory = self.factory

        control.onLoad( self.update_object )

        parent.add( control )
        self.control = control
        self.set_tooltip()

# EOF -------------------------------------------------------------------------
