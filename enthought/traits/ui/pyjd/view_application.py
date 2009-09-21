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

""" Defines a Pyjamas web application, using information from the specified
    View object.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import traceback

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The Pyjamas App object:
app = None

#------------------------------------------------------------------------------
#  Creates a Pyjamas web application for display of the specified View:
#------------------------------------------------------------------------------

def view_application(context, view, kind, handler, id, scrollable, args):
    """ Creates a Pyjamas application to display a specified traits UI
    View.

    Parameters
    ----------
    context : object or dictionary
        A single object or a dictionary of string/object pairs, whose trait
        attributes are to be edited. If not specified, the current object is
        used.
    view : view object
        A View object that defines a user interface for editing trait attribute
        values.
    kind : string
        The type of user interface window to create. See the
        **enthought.traits.ui.view.kind_trait** trait for values and
        their meanings. If *kind* is unspecified or None, the **kind**
        attribute of the View object is used.
    handler : Handler object
        A handler object used for event handling in the dialog box. If
        None, the default handler for Traits UI is used.
    scrollable : Boolean
        Indicates whether the dialog box should be scrollable. When set to
        True, scroll bars appear on the dialog box if it is not large enough
        to display all of the items in the view at one time.

    """
    global app

    if (kind == 'panel') or ((kind is None) and (view.kind == 'panel')):
        kind = 'modal'

#    if app is None:
#        app = Window() # wx.GetApp()

    # TODO: Check if the application is already running.
    if app is None:
        return ViewApplication(context, view, kind, handler, id,
                               scrollable, args).ui.result
    else:
        return view.ui(context, kind=kind, handler=handler, id=id,
                       scrollable=scrollable, args=args).result

#-------------------------------------------------------------------------------
#  "ViewApplication" class:
#-------------------------------------------------------------------------------

class ViewApplication:
    """ A stand-alone Pyjamas web application.
    """

    #---------------------------------------------------------------------------
    #  Initialises the object:
    #---------------------------------------------------------------------------

    def __init__(self, context, view, kind, handler, id, scrollable, args):
        """ Initialises the object.
        """
        self.context = context
        self.view = view
        self.kind = kind
        self.handler = handler
        self.id = id
        self.scrollable = scrollable
        self.args = args

        # TODO: Enable FBI.

        self.ui = ui = self.view.ui( self.context,
                                     kind       = self.kind,
                                     handler    = self.handler,
                                     id         = self.id,
                                     scrollable = self.scrollable,
                                     args       = self.args )

#        self.mainloop()

    #---------------------------------------------------------------------------
    #  Handles application initialization:
    #---------------------------------------------------------------------------

    def OnInit ( self ):
        """ Handles application initialisation.
        """
        self.ui = self.view.ui( self.context,
                                kind       = self.kind,
                                handler    = self.handler,
                                id         = self.id,
                                scrollable = self.scrollable,
                                args       = self.args )
        return True

# EOF -------------------------------------------------------------------------

