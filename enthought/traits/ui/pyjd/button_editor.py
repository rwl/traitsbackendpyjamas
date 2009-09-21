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

""" Define the Pjjamas implementation of the various button editors and the
    button editor factory.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from pyjamas.ui.Button import Button

from enthought.traits.trait_base import \
    user_name_for

from editor import \
    Editor

#------------------------------------------------------------------------------
#  'SimpleEditor' class:
#------------------------------------------------------------------------------

class SimpleEditor ( Editor ):

    #--------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        label = self.factory.label
        if label == '':
            label = user_name_for( self.name )
        self.control = control = Button( label )#parent,
#                                         text     = label,
#                                         listener = self.update_object )
        parent.add( control )

    #--------------------------------------------------------------------------
    #  Handles the user clicking the button by setting the value on the object:
    #--------------------------------------------------------------------------

    def update_object ( self, event ):
        """ Handles the user clicking the button by setting the factory value
            on the object.
        """
        self.value = self.factory.value

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        pass

# EOF -------------------------------------------------------------------------
