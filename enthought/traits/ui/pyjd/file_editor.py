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
