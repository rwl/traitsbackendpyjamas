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
#  Date:   02/02/2009
#
#------------------------------------------------------------------------------

import Tkinter \
    as tk

from tkFont \
    import families

import tkSimpleDialog

import Tix \
    as tix

#------------------------------------------------------------------------------
#  "FontDialog" class:
#------------------------------------------------------------------------------

class FontDialog(tkSimpleDialog.Dialog):
    """ A toolkit specific dialog for font selection. """

    def __init__(self, parent, title="Choose Font"):
        """ Initialises the font dialog.
        """
        tkSimpleDialog.Dialog.__init__(self, parent, title)



    def body(self, frame):
        """ Creates the dialog body. Returns the widget that should have
            initial focus.
        """
        master = tk.Frame(self)
        master.pack(padx=5, pady=0, expand=1, fill=tk.BOTH )

        title = tk.Label( master, text = "Choose Font" )
        title.pack(side=tix.TOP)
#        title.grid( row = 0, columnspan = 2 )

        # Font family list ----------------------------------------------------

        font_frame = tk.Frame( master )
        font_frame.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        family_var = tix.StringVar()
#        family     = tix.ComboBox( master,
##                                   label = "Font family", labelside = 'top',
#                                   dropdown = 0, variable = family_var,
#                                   options = "label.anchor e" )

        family = tk.Listbox( font_frame,
                             selectmode     = tk.SINGLE,
#                             yscrollcommand = scrollbar.set
                             bg             = "White" )

        scrollbar = tk.Scrollbar( family, orient = tk.VERTICAL )
        family.config( yscrollcommand = scrollbar.set, height=200 )

        scrollbar.config( command = family.yview )
        scrollbar.pack( side = tk.RIGHT, fill = tk.Y )

        family.pack( side = tix.LEFT, expand = 1, fill = tk.BOTH, anchor = tk.S )
#        family.grid( row = 1, column = 0, sticky="nsew" )

        for family_name in families(master):
            family.insert( tix.END, family_name )

        family_var = families(master)[0]

        # Font size spinner ---------------------------------------------------

        size_var = tix.IntVar()

        size     = tix.Control( font_frame,
#                                label = "Font Size", labelside = 'top',
                                integer = 1, min = 2, max = 80,
                                variable = size_var,
                                options = "label.anchor e" )

        size.pack( side = tix.RIGHT, anchor = tk.N )
#        size.grid( row = 1, column = 1, sticky=tk.E )

        # Example text --------------------------------------------------------

        example = tix.Text( master, height=3, width = 52, bg = "White" )
        example.pack(side=tk.TOP, fill=tix.X, anchor=tk.N)
#        example.grid( row = 2, columnspan = 2 )

        example.tag_config( "center", justify = tix.CENTER )
        example.insert(tix.END, "This is example text.\n", "center")
        example.insert(tix.END,
            "If you like this text, it can be your font.", "center")

        def on_select( event ):
            example.config( font = ( family_var, size_var.get() ) )

#        family.config( command = on_select )
#        family.config( command = on_select )

        return size # Given initial focus.


    def buttonbox(self):
        ''' Adds a button box in the style of Git GUI.
        '''
        box = tix.Frame(self)

        w = tix.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tix.LEFT, padx=5, pady=5)

        w = tix.Button(box, text="Select", width=10, command=self.ok,
                   default=tix.ACTIVE)
        w.pack(side=tix.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side=tix.RIGHT, padx=5, pady=5, anchor=tk.S)


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


if __name__ == "__main__":
    root = tix.Tk()
    dlg = FontDialog(root, title="Choose Font")

# EOF -------------------------------------------------------------------------
