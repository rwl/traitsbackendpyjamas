#------------------------------------------------------------------------------
#  Copyright (c) 2009 Richard Lincoln
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

from pyjamas.ui \
    import Panel, Dialog, ListBox, Label, TextBox, TextArea, Button

#------------------------------------------------------------------------------
#  "FontDialog" class:
#------------------------------------------------------------------------------

class FontDialog(Dialog):
    """ A toolkit specific dialog for font selection.
    """

    def __init__(self):
        """ Initialises the font dialog.
        """
        Dialog.__init__(self)
        self.setTitle( "Choose Font" )
        self.body(self)
        self.buttonbox()


    def body(self, frame):
        """ Creates the dialog body. Returns the widget that should have
            initial focus.
        """

        title = Label( text = "Choose Font" )
        frame.add( title )

        # Font family list ----------------------------------------------------

        family = ListBox()
        family.setMultipleSelect( False )
        family.setStyleName( "color", "#ffffff" )

        for family_name in families(master):
            family.addItem( item = family_name )

        # Font size spinner ---------------------------------------------------

        size = TextBox()
        frame.add( size )

        # Example text --------------------------------------------------------

        example = TextArea()

        example.addText( "This is example text.\n" )
        example.addText( "If you like this text, it can be your font." )

        def on_select( event ):
            idx = familt.getSelectedIndex()
            example.setStyleName( "font", family.getValue(idx) )
            example.setStyleName( "em", size.getText() )

        family.addChangeListener( on_select )

        return size # Given initial focus.


    def buttonbox(self):
        ''' Adds a button box to the dialog.
        '''
        box = Panel()

        cancel = Button( html = "Cancel", listener = self.cancel )
        box.add( cancel )

        ok = Button( html = "Select", listener = self.ok )
        box.add( ok )

#        self.addKeyboadListener( self.ok, "<Return>" )
#        self.addKeyboadListener( self.cancel, "<Escape>" )

        self.add( box )


    def validate(self):
        ''' Validate the data. This method is called automatically to validate
            the data before the dialog is destroyed.
        '''
        return 1


    def apply(self):
        ''' Process the data. This method is called automatically to process
        the data, *after* the dialog is destroyed.
        '''
        pass

# EOF -------------------------------------------------------------------------
