#------------------------------------------------------------------------------
#
#  Copyright (c) 2008, Richard W. Lincoln
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Author: Richard W. Lincoln
#  Date:   28/01/2008
#
#------------------------------------------------------------------------------

""" Creates a Tkinter GUI application, using information from the specified
View object.

"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tkinter
import traceback

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The Tk App object:
app = None

#------------------------------------------------------------------------------
# Detect if we've been called while within Tkinter's mainloop
#------------------------------------------------------------------------------

def getTkinterLocation():
    """ Returns the location of the Tkinter module. """

    if Tkinter.__file__.endswith('pyc'):
        return Tkinter.__file__[:-1]
    return Tkinter.__file__


def inTkinterMainloop():
    """ Returns true if we're called in the context of Tkinter's
        mainloop(), and false otherwise. """

    stack = traceback.extract_stack()
    tkinter_file = getTkinterLocation()
    for (file_name, lineno, function_name, text) in stack:
        if (file_name, function_name) == (tkinter_file, 'mainloop'):
            return 1
    return 0

#------------------------------------------------------------------------------
#  Creates a Tkinter web application for display of the specified View:
#------------------------------------------------------------------------------

def view_application(context, view, kind, handler, id, scrollable, args):
    """ Creates a Tkinter application to display a specified traits UI
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

    if app is None:
        app = Tkinter.Tk() # wx.GetApp()

    # TODO: Check if the application is already running.
    if (app is None) or (not inTkinterMainloop()):
        return ViewApplication(context, view, kind, handler, id,
                               scrollable, args).ui.result
    else:
        return view.ui(context, kind=kind, handler=handler, id=id,
            scrollable=scrollable, args=args).result

#-------------------------------------------------------------------------------
#  "ViewApplication" class:
#-------------------------------------------------------------------------------

class ViewApplication(Tkinter.Tk):
    """ A stand-alone Tkinter GUI application. """

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__(self, context, view, kind, handler, id, scrollable, args):
        """ Initializes the object. """

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
        """ Handles application initialization.
        """
        self.ui = self.view.ui( self.context,
                                kind       = self.kind,
                                handler    = self.handler,
                                id         = self.id,
                                scrollable = self.scrollable,
                                args       = self.args )
        return True

# EOF -------------------------------------------------------------------------
